import logging
import unittest
from enum import IntEnum
from threading import Thread

import os

import time

from devices import USBDeviceConnection, UpgradableDevice
from event import EventHook
from progress import ProgressSpan, CompositeProgress
from ymodem import LightYModemClient
logger = logging.getLogger(__name__)


use_mock = False


class UpdateFirmwareTask:
    """
    Describes the firmware update process for a single file to a specific device.
    """
    def __init__(self, filename, connection, device):
        self.filename = filename
        self.progress_ = self._build_progress()
        self.connection = connection
        self.device = device
        self.thread = None

    def _build_progress(self):
        size = os.path.getsize(self.filename)
        return ProgressSpan(size, name=os.path.basename(self.filename))

    def start(self):
        logger.info("starting ymodem transfer of file %s" % self.progress.name)
        file = open(self.filename, 'rb')
        result = self.do_update(file)
        self.connection.close()
        self.connection.wait_connected(30)
        return result

    def do_update(self, file):
        client = LightYModemClient()
        if use_mock:
            p = self.progress
            x = p.min
            while x <= p.max:
                self.progress.update(x)
                time.sleep(0.01)
                x += 1024*2
            p.update(p.max)
            result = True
        else:
            result = client.transfer(file, self.connection.enter_ymodem_mode(), self.progress)
            time.sleep(5)
        return result

    @property
    def progress(self):
        return self.progress_

    @property
    def firmware_file(self):
        return self.filename




class Updater:
    def start(self, progress:ProgressSpan, connection:USBDeviceConnection, device:UpgradableDevice):
        files = device.system_modules()
        tasks = [UpdateFirmwareTask(f, connection, device) for f in files]
        CompositeProgress([task.progress for task in tasks], progress)
        for task in tasks:
            task.start()


class FlashState(IntEnum):
    not_connected = 1
    not_started = 2
    in_progress = 3
    error = 4
    complete = 5


class UpdaterState:
    """
    UpdaterState for the entire update process.
    """
    def __init__(self):
        self.on_change = EventHook()
        self.state = None
        self.set_state(FlashState.not_connected)

    def set_state(self,state):
        old = self.state
        self.state = state
        if old!=state:
            self.notify()

    def notify(self):
        self.on_change.fire(self)


class UpdaterStateTest(unittest.TestCase):
    called = False

    def test_change_state_is_published(self):
        s = UpdaterState()

        def handler(item):
            item.called = True
        s.on_change += lambda source: handler(self)
        s.set_state(FlashState.in_progress)
        self.assertTrue(self.called)
