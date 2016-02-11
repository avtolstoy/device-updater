import unittest

from event import EventHook


class SetManager:
    def __init__(self):
        self.devices = set()
        self.events = EventHook()

    def update(self, current):
        scanned_devices = set(current)
        added = scanned_devices-self.devices
        removed = self.devices-scanned_devices
        self.devices -= removed
        self.devices |= added
        for d in removed:
            self.events.fire(d, False)
        for d in added:
            self.events.fire(d, True)


class SetManagerTest(unittest.TestCase):

    def __init__(self, name):
        super().__init__(name)
        self.mgr = SetManager()
        self.mgr.events += lambda item,state: self.manager_events(item,state)
        self.added = []
        self.removed = []

    def manager_events(self, device, added):
        (self.added if added else self.removed).append(device)

    def test_no_change(self):
        self.mgr.update(list())
        self.assertState([], [])

    def test_added(self):
        self.mgr.update([1,2])
        self.assertState([1,2], [])

    def test_added_and_removed(self):
        self.mgr.update([1,2])          # add 1, 2
        self.assertState([1,2], [])
        self.mgr.update([1])            # remove 2
        self.assertState([], [2])
        self.mgr.update([3])            # add 3, remove 1
        self.assertState([3], [1])

    def assertState(self, added, removed):
        self.assertEqual(self.removed, removed)
        self.assertEqual(self.added, added)
        self.removed = []
        self.added = []