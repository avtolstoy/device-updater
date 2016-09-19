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
# Use a mock updater rather than the real thing (saves wearing a device's flash memory)


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
            big_delay = False
            while x <= p.max:
                self.progress.update(x)
                time.sleep(0.01)
                if not big_delay and x>p.max/2:
                    time.sleep(5)
                    big_delay = True
                x += 1024*2
            p.update(p.max)
            result = True
        else:
            channel = self.connection.enter_ymodem_mode()
            client.wait_until_ready(channel)
            result = client.transfer(file, channel, self.progress)
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
    """
    the device is recognized but not supported.
    """
    not_supported_device = 2
    """
    device has a newer or equal version already installed.
    """
    already_upgraded = 3
    """
    user has to flash another version first
    """
    manual_upgrade_needed = 4
    not_started = 20
    in_progress = 30
    error = 40
    complete = 50


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
