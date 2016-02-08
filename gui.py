from kivy.properties import StringProperty, ObjectProperty

import kivy
from app import ConnectedDeviceModel
from kivy.clock import Clock

from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.widget import Widget

kivy.require('1.9.1')

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '180')


class ConnectedDevice(Label):
    text = StringProperty("hi")
    device = ObjectProperty(None, allownone=True)
    go = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ConnectedDevice, self).__init__(**kwargs)
        self.model = ConnectedDeviceModel(self)                     # the device model using this instance as the view
        self.go.bind(on_press=lambda a:self.start())                # go button clicked
        self.bind(device=lambda instance,value:self.device_changed()) # observe changes to device
        self.device_changed()                                             # trigger first update
        Clock.schedule_interval(lambda dt:self.trigger(), 1)

    def trigger(self):
        self.model.update()

    def update(self, item):
        """Notification from the ConnectedDeviceModel"""
        self.device = item

    def start(self):
        self.go.text = "Doing it!"

    def device_changed(self):
        self.text = "Connected" if self.device else "Disconnected"


class Gui(App):

    def build(self):
        return ConnectedDevice()

if __name__ == '__main__':
    Gui().run()