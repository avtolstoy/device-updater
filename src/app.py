"""
The updater application logic. This is independent from the UI used (console, GUI)
"""

import logging
import unittest
from abc import abstractmethod
from threading import Thread, Event

from controller import Actor, ActiveObjectProxy
from devices import UpgradableDevice, USBDeviceConnection
from progress import ProgressSpan
from serial_scan import USBScanner
from set_manager import SetManager
from updater import Updater, UpdaterState, FlashState

logger = logging.getLogger(__name__)

# text "To start updating your device, conenct it to your computer via a USB cable. ??"
# image is electron greyed out and slightly translucent
# when the device is connected, the image moves to the left, a cable and laptop appear
# for now, no device info. later versions will display details of the connected device.
# text changes "To update your device, click on the update button."
# as the device updates, it blinks the magenta LED
# as the device updates, lights flow along the USB cable.
# the round updater button fills in as the update progresses.
# when the update is complete, button changes to complete.
# disconnecting the device resets the system.

# monitor serial connections every second to determine which devices are available and publish that as donnect/disconnect events.

# connect/disconenct passed through a filter of interesting devices
# map from VID/PID to device type.
# maintains a list of USB devices so the same device is featured in the disconnect method.

# refactor ymodem class to provide bytes transferred progress


def relative_file(path):
    return path


class Devices:
    photon = UpgradableDevice("Photon", 0x2b04, 0xc006, "photon", "0.5.0", 2)
    electron = UpgradableDevice("Electron", 0x2b04, 0xc00a, "electron", "0.5.0", 2)
    none = []
    all = [ photon, electron ]


class DevicesTest(unittest.TestCase):
    def test_device_resource(self):
        for d in Devices.all:
            modules = d.system_modules(force=True)
            for m in modules:
                f = open(m, "rb")
                f.close()


class UpdaterEvents:
    @abstractmethod
    def connected_device_changed(self, device):
        pass

    @abstractmethod
    def updater_state_changed(self, state:FlashState):
        pass

    @abstractmethod
    def error(self, error):
        pass

    @abstractmethod
    def progress(self, min, max, current):
        pass


def create_threaded_controller(callback:UpdaterEvents):
    target = UpdaterController(callback)
    actor = Actor()
    actor.setDaemon(True)
    actor.exception_handler = lambda cmd,args,kwargs,e: callback.error(e)
    actor.start()
    proxy = ActiveObjectProxy(actor, target)
    target._set_thread_proxy(proxy)
    return proxy


class UpdaterController:
    def __init__(self, callback:UpdaterEvents):
        self.model = ConnectedDeviceModel(self)                     # the device model using this instance as the view
        # we pass in the proxy because the device model runs on a separate thread, but we want updates to fire on the main controller thread.
        self.callback = callback
        self.scan_thread = None
        self.updater_state = UpdaterState()
        self.updater_state.on_change += lambda source: self._updater_state_changed(self.updater_state.state)
        self.updater_state.on_change += lambda source: callback.updater_state_changed(self.updater_state.state)
        self.updater_state.notify()     # trigger initial update

    def _set_thread_proxy(self, proxy):
        # rather than using self to handle updates, use the proxy so updates are processed on the controller thraed rather than
        # the background scanner thread
        self.model.view = proxy

    def _updater_state_changed(self, state):
        if state not in [ FlashState.in_progress, FlashState.error ]:
            self.start_scan(0.25)
        else:
            self.stop_scan()

    def update(self, device):
        self.callback.connected_device_changed(device)
        self.updater_state.set_state(FlashState.not_started if device else FlashState.not_connected)

    def scan(self):
        self.model.update()

    def flash(self, connected):
        try:
            self.updater_state.set_state(FlashState.in_progress)
            if connected is None:
                raise ValueError("No device connected")
            connection = USBDeviceConnection(*connected)
            progress = ProgressSpan()
            def progress_update(current):
                self.callback.progress(progress.min, progress.max, progress.current)
            progress.on_change += progress_update
            Updater().start(progress, connection, connection.device)
            self.updater_state.set_state(FlashState.complete)
        except:
            self.updater_state.set_state(FlashState.error)
            raise

    def start_scan(self, period):
        self.stop_scan()
        event = Event()
        scan_thread = Thread(name="usb scan", target=self._background_scan, args=[period, event], daemon=True)
        scan_thread.event = event
        self.scan_thread = scan_thread
        scan_thread.start()

    def stop_scan(self):
        t = self.scan_thread
        if t:
            t.event.set()
            t.join()

    def _background_scan(self, period, stop_event:Event):
        while not stop_event.is_set():
            self.scan()
            stop_event.wait(period)
        self.scan_thread = None


class ConnectedDeviceModel:
    """
    Keeps track of the first device connected, until it becomes disconnected.
    The client is responsible for calling update() regularly. The connected attribute is (port, USBDevice) or None when
    no connected device.

    """
    def __init__(self, view, known_devices=Devices.all):
        """
        :param view: called with update((port,device)) when a device is connected and update(None) when disconnected
        """
        self.view = view
        self.connected = None
        self.scan = USBScanner(known_devices)
        self.mgr = SetManager()
        self.mgr.events += lambda item,added: self.device_changed(item, added)

    def device_changed(self, item, added):
        if added != self.connected:     # when added, we don't have a connection, and when removed we do
            self.connected = (item if added else None)
            self.view.update(self.connected)

    def update(self):
        current = self.scan.scan()
        self.mgr.update(current)


class ConnectedDeviceModelTest(unittest.TestCase):
    connected = None

    def update(self, device):       # implements the view contract expected by ConnectedDeviceModel
        self.connected = device

    def test_update(self):
        m = ConnectedDeviceModel(self, Devices.none)
        m.update()
        self.assertEqual(self.connected, None)
        m.mgr.update([Devices.photon])              # simulate a connected device
        self.assertEqual(self.connected, Devices.photon)

if __name__ == '__main__':
    unittest.main()
