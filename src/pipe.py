

"""
Implements an in-memory pipe. The pipe is expected to buffer data between threads using pre-emptive or co-operative
multitasking.
"""
import asyncio
import threading
import unittest
from io import RawIOBase, IOBase


class BasePipe(RawIOBase):

    def __init__(self, cv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cv = cv
        self.data = None

    def readable(self, *args, **kwargs):
        return True

    def writable(self, *args, **kwargs):
        return True

    def read(self, size=1):
        with self.cv:
            while self.data is None and not self.closed:
                self.cv.wait()
            result = self.data
            self.data = None
            self.cv.notify()
            return result if result is not None else bytes()

    def write(self, data):
        for b in data:
            with self.cv:
                while self.data is not None and not self.closed:
                    self.cv.wait()
                super()._checkClosed()
                self.data = bytes([b])
                self.cv.notify()

    def close(self):
        with self.cv:
            while self.data is not None and not self.closed:
                self.cv.wait()
            super().close()
            self.cv.notify()


class ThreadedPipe(BasePipe):
    def __init__(self, *args, **kwargs):
        super().__init__(threading.Condition(), *args, **kwargs)


class AsyncIOPipe(BasePipe):
    def __init__(self, *args, **kwargs):
        super().__init__(asyncio.Condition(), *args, **kwargs)


class ThreadPipeTest(unittest.TestCase):

    def write(self, pipe, data):
        pipe.write(data)
        pipe.close()

    def test_pipe(self):
        data = bytes(b'123456')
        pipe = ThreadedPipe()
        thread = threading.Thread(target=self.write,args=(pipe, data))
        thread.start()
        result = pipe.readall()
        thread.join()
        self.assertEqual(result, data)

    def test_can_read_on_close(self):
        pipe = ThreadedPipe()
        byte1 = bytes(b'1')
        thread = threading.Thread(target=self.write,args=(pipe, byte1))
        thread.start()
        self.assertEqual(pipe.read(), byte1)
        self.assertEqual(pipe.read(), bytes())
        thread.join()


class RWPair(IOBase):
    def __init__(self, reader, writer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not reader.readable():
            raise OSError('"reader" argument must be readable.')
        if not writer.writable():
            raise OSError('"writer" argument must be writable.')
        self.reader = reader
        self.writer = writer

    def read(self, size=1):
        return self.reader.read(size)

    def readinto(self, b):
        return self.reader.readinto(b)

    def write(self, b):
        return self.writer.write(b)

    def peek(self, size=0):
        return self.reader.peek(size)

    def read1(self, size):
        return self.reader.read1(size)

    def readable(self):
        return self.reader.readable()

    def writable(self):
        return self.writer.writable()

    def flush(self):
        return self.writer.flush()

    def close(self):
        self.writer.close()

    def isatty(self):
        return self.reader.isatty() or self.writer.isatty()

    @property
    def closed(self):
        return self.writer.closed

