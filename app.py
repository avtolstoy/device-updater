from serial_scan import USBDevice, USBScanner
from set_manager import SetManager


class ConnectedDeviceModel:
    """
    Keeps track of the first device connected, until it becomes disconnected.
    The client is responsible for calling update() regularly.
    """
    photon = USBDevice("Photon", 0x2b04, 0xc006)
    known_devices = [ photon ]

    def __init__(self, view):
        """
        :param view: called with update(device) when a device is connected and update(None) when disconnected
        """
        self.view = view
        self.connected = None
        self.scan = USBScanner(self.known_devices)
        self.mgr = SetManager()
        self.mgr.events += lambda item,added: self.device_changed(item, added)

    def device_changed(self, item, added):
        if added != self.connected:     # when added, we don't have a connection, and when removed we do
            self.connected = (item if added else None)
            self.view.update(self.connected)

    def update(self):
        current = self.scan.scan()
        self.mgr.update(current)
