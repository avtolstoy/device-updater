import logging
import unittest

import re
from serial import Serial
from serial.tools import list_ports
from support import CommonEqualityMixin

logger = logging.getLogger(__name__)


class USBDevice(CommonEqualityMixin):
    """ Represents a USB device
    """
    def __init__(self, name, vid, pid):
        self.name = name
        self.vid = vid
        self.pid = pid

    def matches(self, vid, pid):
        return self.vid == vid and self.pid == pid

    def __hash__(self):
        return self.vid*23+self.pid+hash(self.name)


class USBScanner:
    def __init__(self, known_devices):
        """
        :param known_devices:   A list of USBDevice instances
        """
        self.known_devices = known_devices

    def scan(self):
        """
        :return: an iterable of (port, device) listing the current set of connected devices
        """
        return self.find_known_devices(self.serial_port_info())

    def find_known_devices(self, ports):
        for p in ports:
            d = self._known_device(*p)
            if d:
                yield d

    def _known_device(self, port, name, vid, pid):
        """
        :return: A tuple (port, USBDevice) or None
        """
        for d in self.known_devices:
            if d.matches(vid, pid):
                return port, d
        return None

    @staticmethod
    def serial_port_info():
        """
        :return: a tuple of serial port info tuples (port, name, desc)
        """
        for p in list_ports.comports():
            dev = (p.device, p.name, p.vid, p.pid)
            yield dev


class USBScannerTest(unittest.TestCase):
    dev1 = USBDevice("ultiMat", 1, 2)
    dev2 = USBDevice("ultiMat2", 3, 4)
    devs = [dev1, dev2]
    scanner = USBScanner(devs)

    def test_first_device_matches(self):
        self.assertEqual(list(self.scanner.find_known_devices([("com", "asjfkj", 1, 2)])), [("com", self.dev1)])

    def test_second_device_matches(self):
        self.assertEqual(list(self.scanner.find_known_devices([("com2", "asjfkj", 3, 4)])), [("com2", self.dev2)])

    def test_second_device_fail(self):
        self.assertEqual(list(self.scanner.find_known_devices([("com2", "asjfkj", 3, 5)])), [])
        self.assertEqual(list(self.scanner.find_known_devices([("com2", "asjfkj", 4, 3)])), [])


class USBScannerIntegrationTest(unittest.TestCase):
    dev1 = USBDevice("Photon", 0x2b04, 0xc006)
    devs = [dev1]
    scanner = USBScanner(devs)

    def test_photon_detected(self):
        self.assertEqual(list(self.scanner.scan())[0][1], self.dev1)

    test_photon_detected.photon = True  # conditionally enable this tet

    def test_usb_device_hashable(self):
        set(self.devs)



if __name__ == '__main__':
    unittest.main()
