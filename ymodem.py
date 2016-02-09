import logging
import unittest

import time

import io
from io import RawIOBase
from threading import Thread

import os
import sys
import serial
from pipe import ThreadedPipe, RWPair
from progress import ProgressSpan

logger = logging.getLogger(__name__)


def asbyte(v):
    return bytes([(v & 0xFF)])

def asstring(b):
    return b.decode('ascii')

def tobytes(s):
    return s.encode('ascii', 'ignore')


class LightYModemProtocol:
    """
    Receive_Packet
    - first byte SOH/STX (for 128/1024 byte size packets)
    - EOT (end)
    - CA CA abort
    - ABORT1 or ABORT2 is abort

    Then 2 bytes for seq-no (although the sequence number isn't checked)

    Then the packet data

    Then CRC16?

    First packet sent is a filename packet:
    - zero-terminated filename
    - file size (ascii) followed by space?
    """

    soh = 1  # 128 byte blocks
    stx = 2  # 1K blocks
    eot = 4
    ack = 6
    nak = 0x15
    ca = 0x18  # 24
    crc16 = 0x43  # 67
    abort1 = 0x41  # 65
    abort2 = 0x61  # 97

    packet_len = 1024
    expected_packet_len = packet_len + 5
    packet_mark = stx


class LightYModemClient(LightYModemProtocol):
    default_file_name = 'binary'

    def __init__(self):
        self.progress = None
        self.seq = 0  # current packet sequence count
        self.channel = None  # The stream the protocol is sent over
        self.closing = False

    def flush(self):
        pass

    def blocking_read(self):
        ch = None
        while not ch:
            ch = self.channel.read()
        return ch[0]

    def _read_response(self):
        ch1 = self.blocking_read()
        if ch1 == LightYModemClient.ack and self.seq == 0 and not self.closing:  # may send also a crc16
            ignore = self.blocking_read()
        elif ch1 == LightYModemClient.ca:  # cancel, always sent in pairs
            ignore = self.blocking_read()
        return ch1

    def write(self, packet):
        self.channel.write(packet)
        return len(packet)

    def _send_ymodem_packet(self, data):
        # pad string to 1024 chars
        data = data.ljust(self.packet_len)
        seqchr = asbyte(self.seq & 0xFF)
        seqchr_neg = asbyte((-self.seq - 1) & 0xFF)
        crc16 = b'\x00\x00'
        packet = asbyte(self.packet_mark) + seqchr + seqchr_neg + data + crc16
        if len(packet) != self.expected_packet_len:
            raise Exception("packet length is wrong!")

        written = self.write(packet)
        logger.debug("sent packet data, flush..." + str(written))
        self.flush()
        logger.debug("wait response..")
        response = self._read_response()
        if response == LightYModemClient.ack:
            logger.debug("sent packet nr %d " % self.seq)
            self.seq += 1
        return response

    def _send_close(self):
        self.channel.write(asbyte(LightYModemClient.eot))
        self.flush()
        response = self._read_response()
        if response == LightYModemClient.ack:
            logger.debug("sending empty filename header to close session")
            self.closing = True
            self.seq = 0
            self.send_filename_header("", 0)
            self.channel.close()

    def send_packet(self, file):
        response = LightYModemClient.eot
        data = file.read(LightYModemClient.packet_len)
        if len(data):
            response = self._send_ymodem_packet(data)
            self.progress += len(data)
        return response

    def send_filename_header(self, name, size):
        packet = tobytes(name) + asbyte(0) + tobytes(str(size)) + bytes([0x20])
        return self._send_ymodem_packet(packet)

    def transfer(self, file, channel:RawIOBase, progress:ProgressSpan):
        """
        Transfers a single file to the device and closes the session, so the device places the data in the
        target location.

        file: the file to transfer via ymodem
        channel: the ymodem endpoint
        progress: notification of progress
        """
        self.seq = 0
        self.channel = channel
        self.progress = progress

        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        progress.min = 0
        progress.max = size
        progress.update(0)

        response = self.send_filename_header(self.default_file_name, size)
        while response == LightYModemClient.ack:
            response = self.send_packet(file)
        file.close()
        if response != LightYModemClient.eot:
            raise LightYModemException("Unable to transfer the file to the device. Code=%d" % response)
        self._send_close()
        return True

class LightYModemException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

serverlog = logging.getLogger(__name__+".server")

class LightYModemServer(LightYModemProtocol):
    max_errors = 5
    packet_seqno_index = 1
    packet_seqno_comp_index = 2
    packet_header_length = 3
    packet_trailer_length = 2
    packet_overhead = packet_header_length + packet_trailer_length
    packet_size = 128
    packet_large_size = 1024
    file_name_Length = 256
    file_size_length = 16

    def __init__(self, channel, file_handler):
        self.channel = channel
        self.file_handler = file_handler
        self.packets_received = 0
        self.session_done = False
        self.file_done = False
        self.file_started = False
        self.errors = 0

    def receive(self):
        """
        :param file_handler: called with (filename,length), receives a writable for the file contents
        """
        self.packets_received = 0
        while not self.session_done:
            self.receive_file()

    def _send_cancel(self):
        self.send_byte(self.ca)
        self.send_byte(self.ca)

    def cancel_file(self):
        self.file_done = True
        self._send_cancel()

    def cancel_session(self):
        self.session_done = True
        self.cancel_file()

    def send_byte(self, b):
        self.channel.write(asbyte(b))

    def receive_byte(self, timeout):
        end = time.perf_counter()+timeout
        b = self.channel.read()
        while len(b)==0 and time.perf_counter()<end:
            b = self.channel.read()
        if len(b)==0:
            raise IOError("timeout")
        return b[0]

    def receive_file(self, timeout=3):
        self.file_done = False
        self.file_started = False
        self.errors = 0
        self.packets_received = 0
        serverlog.debug("starting receive_file")
        while not self.file_done:
            code, packet, length = self._receive_packet(timeout)
            if code == self.packet_ok:
                self.errors = 0
                self._handle_packet(packet, length)
            elif code == self.packet_cancelled:
                self.cancel_session()
                raise IOError("interrupted")
            elif code == self.packet_ignored:
                self.send_byte(self.ack)
            elif code == self.packet_done:
                serverlog.debug("file received")
                self.send_byte(self.ack)  # end of transmission
                serverlog.debug("file received - ack sent")
                self.file_done = True
            else:
                if self.file_started:
                    self.errors += 1
                    self.send_byte(self.crc16)
                if self.errors > self.max_errors:
                    self.cancel_session()
                    raise IOError("too many errors")

    packet_ok = 0
    packet_cancelled = 1
    packet_ignored = 2
    packet_error = -1
    packet_done = 3
    space = ord(' ')

    def _receive_packet(self, timeout):
        b = self.receive_byte(timeout)
        serverlog.debug("got packet byte %d" % b)
        if b == self.soh:
            return self._read_packet_data(self.packet_size, timeout, b)
        elif b == self.stx:
            return self._read_packet_data(self.packet_large_size, timeout, b)
        elif b == self.eot:
            return self.packet_done, None, None
        elif b == self.ca:
            b = self.receive_byte(timeout)
            if b == self.ca:
                return self.packet_cancelled, None, None
            else:
                return self.packet_error, None, None
        elif b == self.abort1 or b == self.abort2:
            return self.packet_cancelled, None, None
        elif b == self.space:
            return self.packet_ignored, None, None
        else:
            return self.packet_error, None, None

    def _read_packet_data(self, size, timeout, b):
        data = bytearray()
        data.append(b)
        for i in range(1, size+self.packet_overhead):
            data.append(self.receive_byte(timeout))

        if data[self.packet_seqno_index] != ((data[self.packet_seqno_comp_index] ^ 0xFF) & 0xFF):
            serverlog.warn("packet sequence validation error")
            return self.packet_error, None, None
        serverlog.debug("packet received")
        return self.packet_ok, bytes(data), size

    def _handle_packet(self, packet_data, packet_length):
        if (packet_data[self.packet_seqno_index] & 0xff) != (self.packets_received & 0xff):
            serverlog.warn("packet sequence index does not match: expected %d, was %d" % ( self.packets_received & 0xff, packet_data[self.packet_seqno_index] & 0xff ))
            self.send_byte(self.nak)
        else:
            self._handle_valid_packet(packet_data, packet_length)

    def _handle_valid_packet(self, packet_data, packet_length):
        if not self.packets_received:  # filename packet
            serverlog.debug("handling file header packet")
            self._handle_file_header_packet(packet_data, packet_length)
        else:  # data packet
            serverlog.debug("handling regular packet")
            self.file_store.write(packet_data[self.packet_header_length:self.packet_header_length + packet_length])
            self.send_byte(self.ack)
        self.packets_received += 1
        self.file_started = True

    def _handle_file_header_packet(self, packet_data, packet_length):
        serverlog.debug("file header packet received")
        if packet_data[self.packet_header_length]:
            file_name, file_len = self._parse_file_packet(packet_data[self.packet_header_length:])
            self.file_store = self.file_handler(file_name, file_len)
            if self.file_store is None:
                self.cancel_session()
            self.send_byte(self.ack)
            self.send_byte(self.crc16)
            serverlog.debug("file begin {},size={}".format(file_name, file_len))

        else:  # filename packet is empty - end session
            serverlog.debug("received empty file header, ending session")
            self.send_byte(self.ack)
            serverlog.debug("received empty file header, ack sent")
            self.file_done = True
            self.session_done = True

    @staticmethod
    def _parse_file_packet(packet_data):
        end_of_name = packet_data.find(0)
        file_name = packet_data[0:end_of_name]
        end_of_length = packet_data.find(32, end_of_name)  # find space
        file_length = packet_data[end_of_name + 1:end_of_length]
        return asstring(file_name), int(asstring(file_length))


class LightYModemTest(unittest.TestCase):
    def start_client(self, file, channel, progress):
        client = LightYModemClient()
        result = client.transfer(open(file, 'rb'), channel, progress)
        channel.close()
        self.assertEqual(result, True)
        logger.debug("server test: client thread exiting")

    def test_transfer(self):
        p1 = ThreadedPipe()
        p2 = ThreadedPipe()
        progress = ProgressSpan()
        client_channel = RWPair(p1, p2)
        server_channel = RWPair(p2, p1)
        file = 'ymodem.py'
        to_receive = [(LightYModemClient.default_file_name, os.path.getsize(file), file)]
        self.to_receive = to_receive
        self.files = {}
        t = Thread(target=self.start_client, args=(file, client_channel, progress))
        t.start()
        server = LightYModemServer(server_channel, lambda filename, length: self.add_file(filename, length))
        server.receive()
        server_channel.close()
        self.assertEqual(len(self.files), 1, "expected 1 file transferred")
        self.check_received(to_receive)

    def add_file(self, filename, length):
        # remove the first item and validate it matches
        file = self.to_receive.pop(0)
        self.assertEqual(file[0], filename)
        self.assertEqual(file[1], length)
        buffer = io.BytesIO()
        self.files[filename] = buffer
        return buffer

    def check_received(self, files):
        for f in files:
            actual = self.files[f[0]]
            expected = open(f[2], "rb")
            self.assertEqual(actual.readall(), expected.readall())


def ymodem(args):
    port = args[1]
    filename = args[2]
    ser = serial.Serial(port, baudrate=28800)
    file = open(filename, 'rb')
    result = LightYModemClient().transfer(file, ser, sys.stderr)
    file.close()
    print("result: " + str(result))

    try:
        while (True):
            print(ser.read())
    except:
        pass
    print("Done")


if __name__ == '__main__':
    ymodem(sys.argv)
