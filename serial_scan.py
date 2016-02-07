import logging
import unittest

import re
from serial import Serial
from serial.tools import list_ports

logger = logging.getLogger(__name__)


class AutoRepr(object):
     def __repr__(self):
         items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
         return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))


class USBDevice(AutoRepr):
    def __init__(self, name, vid, pid):
        self.name = name
        self.id_regex = id_regex


class USBScanner:

    def __init__(self, known_devices):
        """
        :param known_devices:   A list of USBDevice instances
        """
        self.known_devices = known_devices


    def find_known_devices(self, ports):
        for p in ports:
            d = self._known_device(*p)
            if d:
                yield d

    def _known_device(self, port, name, desc):
        """
        :param port:
        :param name:
        :param desc:
        :return: A tuple (port, USBDevice) or None
        """
        for d in self.known_devices:
            if re.match(d.id_regex, desc):
                return port, d
        return None

    @staticmethod
    def serial_port_info():
        """
        :return: a tuple of serial port info tuples (port, name, desc)
        """
        return tuple(list_ports.comports())


class USBScannerTest(unittest.TestCase):

    dev1 = USBDevice("ultiMat", ".*zzz.*")
    dev2 = USBDevice("ultiMat2", ".*yyy.*")
    devs = [dev1,dev2]
    scanner = USBScanner(devs)

    def test_first_device_matches(self):
        self.assertEqual(list(self.scanner.find_known_devices([("com","asjfkj", "azzzb")])), [("com", self.dev1)])

    def test_second_device_matches(self):
        self.assertEqual(list(self.scanner.find_known_devices([("com2","asjfkj", "yyy")])), [("com2", self.dev2)])


class USBScannerIntegrationTest(unittest.TestCase):

    dev1 = USBDevice("Photon", 0x2d04, 0xc006)
    devs = [dev1]


if __name__ == '__main__':
    print(list_ports.comports())
#    unittest.main()
