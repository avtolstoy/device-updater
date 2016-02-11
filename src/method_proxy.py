import logging
import unittest
from types import MethodType

logger = logging.getLogger(__name__)


class MethodWrapperProxy:
    """
    Proxies an object so that calls to an object are routed through a function factory
    """
    def __init__(self, delegate, func_wrapper):
        self.delegate = delegate
        self.func_wrapper = func_wrapper

    def __getattr__(self, aname):
        target = self.delegate
        f = getattr(target, aname)
        if isinstance(f, MethodType):
            return MethodType(self.func_wrapper(self, target, aname, f), self)
        else:
            return f


class RomanticGestures:
    def __init__(self, gift):
        self.gift = gift

    def send(self, to):
        return self.gift + " for "+to


def upper_case_wrapper(proxy, target, name, f):
    def make_upper(self, *args, **kwargs):
        return f(*args,**kwargs).upper()
    return make_upper


class MethodWrapperProxyTest(unittest.TestCase):
    def test_wrapper(self):
        target = RomanticGestures("flowers")
        proxy = MethodWrapperProxy(target, upper_case_wrapper)
        result = proxy.send("you")
        self.assertEqual(result, "FLOWERS FOR YOU")

