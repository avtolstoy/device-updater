import logging
from sys import stdout
from time import sleep

from app import ConnectedDeviceModel
from devices import USBDeviceConnection
from progress import ProgressSpan
from updater import Updater

logger = logging.getLogger(__name__)


class ConsoleView:

    def __init__(self):
        self.connected = None

    def update(self, connected):
        """
        Callback from ConnectedDeviceModel
        :param connected:   The connected device
        """
        self.connected = connected
        if connected:
            logger.info("device connected")
        else:
            logger.info("device disconnected")

output = stdout

def msg(m):
    print(m, file=output)

def main():
    view = ConsoleView()
    model = ConnectedDeviceModel(view)
    model.update()
    if not view.connected:
        msg("Yo dawg, connect a Particle device to USB")
        while not view.connected:
            model.update()
        msg("Rad. Connected device is {} on port {}".format(view.connected[1].name, view.connected[0]))

    device_connection = USBDeviceConnection(*view.connected)
    flash(device_connection)


def flash(connection):
    progress = ProgressSpan()
    progress.on_change += lambda val: print("%d / %d" % (progress.current, progress.max))
    Updater().start(progress, connection, connection.device)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
