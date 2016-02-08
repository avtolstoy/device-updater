from app import ConnectedDeviceModel


class ConsoleView:
    def update(self, device):
        if device:
            print("device connected: "+str(device)+"\n")
        else:
            print("device disconnected: "+str(device)+"\n")


def loop():
    view = ConsoleView()
    model = ConnectedDeviceModel(view)
    while True:
        model.update()


loop()