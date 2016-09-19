"""
Provides UpgradableDevice describes the upgrade details for a given device.
USBDeviceConnection is a proxy to a connected device. Methods for entering listening/ymodem mode.
A Tee can be used to debug the serial connection.
"""

import logging
from sys import stdout, stderr

from io import RawIOBase, TextIOBase

import os
import serial
import time

from serial_scan import USBDevice
from ymodem import LightYModemProtocol

logger = logging.getLogger(__name__)


class UpgradableDevice(USBDevice):
    def __init__(self, name, vid, pid, resource_dir, version, system_parts):
        super().__init__(name, vid, pid)
        self.system_parts = system_parts
        self.version = version
        self.resource_dir = resource_dir

    def resource_path(self, resource=None):
        return os.path.join("resources", self.resource_dir, resource)

    def system_modules(self, force=False):
        """
        :param force: When true, includes all files even if they don't exist
        :return:
        """
        modules = []
        for i in range(0,self.system_parts):
            f = "system-part%d-%s-%s.bin" % (i+1, self.version, self.resource_dir)
            res = self.resource_path(f)
            if force or os.path.isfile(res):
                modules.append(res)
            else:
                logger.error("file resource not found: {}", res)

        return modules


def try_invoke(target, args):
    result, exception = None, None
    try:
        result = target(*args)
    except Exception as e:
        exception = e
    return result, exception


def try_with_timeout(target, args, timeout, pause):
    """
    Attempt an operation as long as it fails up to the given timeout.
    :param target:  The callable
    :param args:    The arguments to pass
    :param timeout: the timeout
    :param pause:   how long to pause between each failed invocation
    :return: either the result from successfully invoking the callable
    raises the exception thrown by the callable on timeout.
    """
    end = time.perf_counter()+timeout
    result, exception = try_invoke(target, args)
    while exception is not None and time.perf_counter()<end:
        time.sleep(pause)
        result, exception = try_invoke(target, args)
    if exception is not None:
        raise exception
    return result


class USBDeviceConnection:

    ymodem_timeout = 0.1
    use_tee = False
    """
    Describes a connection to a device on a given serial port.
    """
    def __init__(self, port, device):
        self.port = port
        self.device = device
        self.serial = None

    def close(self):
        if self.serial:
            self.serial.close()
            self.serial = None

    def open(self, baud, timeout=None):
        self.close()
        self.serial = serial.Serial(self.port, baudrate=baud, timeout=timeout)

    def fetch_version_string(self):
        if self.serial is None:
            self.open(9600, timeout=0.3)
        self.send('v')
        line = self.readline()
        logger.debug("listening: %s" % line)
        self.drain()
        return line

    def is_listening(self):
        """
        Determines if the device is in listening mode. This relies on the 'v' command, which is present in
        system firmware 0.4.4 onwards.
        """
        line = self.fetch_version_string()
        return line.lower().startswith("system firmware version")

    def wait_connected(self, timeout=30, sleep=1):
        return try_with_timeout(self._connect, [], timeout, sleep)

    def _connect(self):
        try:
            self.open(9600, timeout=self.ymodem_timeout)
        except:
            self.close()
            raise

    def enter_ymodem_mode(self, timeout=60, sleep=0.1):
        """
        Repeatedly performs the tests to enter ymodem mode.
        """
        return try_with_timeout(self._enter_ymodem_mode, [], timeout, sleep)

    def _enter_ymodem_mode(self):
        """
        Puts the device in ymodem mode. First we test to see if the device is in listening mode by sending the 'v'
        command to fetch the system firmware version. When in listening mode, the device responds with a line starting
        "system firmware version".
        If the listening mode test is successful, the `f` command is sent to start ymodem transfer.
        If the test for listening mode fails, the line rate is set to trigger ymodem mode. Then a space is sent. The
         device responds with an ACK when in ymodem mode.
        """
        try:
            if self.is_listening():
                self.close()
                self.open(9600, timeout=self.ymodem_timeout)
                self.send('f')
                self.drain()
                time.sleep(0.1)
            else:
                self.open(28800, timeout=self.ymodem_timeout)
                time.sleep(0.1)
                self.drain()
                # check if ymodem is active - a space causes an ACK response
                self.send(' ')
                result = self.serial.read(1)
                if not len(result) or (result[0]!=LightYModemProtocol.ack and result[0]!=LightYModemProtocol.crc16):
                    raise IOError("device not ready for ymodem transfer")
            print(self.use_tee)
            return self.serial if not self.use_tee else Tee(self.serial, stderr, stdout)
        except:
            self.close()
            raise

    def readline(self):
        line = self.serial.readline()
        return asstring(line)

    def send(self, data):
        self.serial.write(asbytes(data))

    def drain(self):
        response = self.readline()
        while response:
            response = self.readline()

def asstring(b):
    """
    >>> asstring(b'1')
    '1'
    >>> asstring('1')
    '1'
    """
    return b.decode('ascii') if type(b) == bytes else b


def asbytes(s):
    """
    >>> asbytes(b'1')
    b'1'
    >>> asbytes('1')
    b'1'
    """
    return s.encode('ascii') if type(s) == str else s


class Tee(TextIOBase):
    def __init__(self, main, dump, peek, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.dump = dump
        self.peek = peek

    def readable(self):
        return self.main.readable()

    def writable(self):
        return self.main.writable()

    def seekable(self, *args, **kwargs):
        return self.main.seekable()

    def read(self, size=1):
        result = self.main.read(size)
        self.dump_read(result)
        return result

    def write(self,  data):
        result = self.main.write(data)
        #self.dump.write(str(data))
        #self.dump.flush()
        return result

    def flush(self, *args, **kwargs):
        result = self.main.flush()
        self.dump.flush()
        self.peek.flush()
        return result

    def readline(self):
        result = self.main.readline()
        self.dump_read(result)

    def dump_read(self, result):
        if result:
            self.peek.write(str(result))
            self.peek.flush()

    def close(self, *args, **kwargs):
        result = self.main.close(*args, **kwargs)
