import os
import sys
import threading

import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.widget import Widget

from app import UpdaterEvents, create_threaded_controller
from method_proxy import MethodWrapperProxy
from spinner import MDSpinner
from updater import FlashState

kivy.require('1.9.1')

from kivy.factory import Factory

Factory.register('MDSpinner', cls=MDSpinner)


def kivy_event_thread_dispatch(proxy, target, name, f):
    """
    a function factory that returns a function that will schedule
    the given function for execution on the event thread.
    """
    def schedule(self, *args, **kwargs):
        def scheduled(dt):
            f(*args, **kwargs)
        Clock.schedule_once(scheduled)
    return schedule


def post_to_event_thread(target):
    """
    proxies a proxy of an interface that delegates to the target by dispatching to the GUI thread
    :param target:  The object to invoke on the GUI thread
    :param widget:  The root widget
    :return: a proxy that can be used on other threads
    """
    return MethodWrapperProxy(target, kivy_event_thread_dispatch)

def large(s):
    return "[b]"+s+"[/b]"

"""
A widget to display the status of a connected device.
"""
class ConnectedDevice(Widget):
    text = StringProperty("")
    go = ObjectProperty(None)       # start update button
    bar = ObjectProperty(None)      # progress bar

    """
    flag to control if this device can be upgraded. The go text will
    show why the device cannot be upgraded.
    """
    upgrade_available = BooleanProperty()

    """
    text on the button to start the flash process.
    """
    go_text = StringProperty("")

    """
    opacity of device info, used to fade in/out
    """
    device_opacity = NumericProperty(0)

    """
    the version to upgrade to
    """
    update_version = StringProperty("")

    """
    the version on the device
    """
    existing_version = StringProperty("")

    """
    the current update state value. see FlashState
    """
    update_state = ObjectProperty(FlashState.not_connected)

    """
    The currently connected device
    """
    device = ObjectProperty(None, allownone=True)

    """
    The current update progress as a value between 0 and 1
    """
    progress = NumericProperty(0)

    """
    Is the flash operation in progress
    """
    in_progress = BooleanProperty(False)

    """
    Set to false when the device is updating but progress has stalled.
    """
    making_progress = BooleanProperty(True)

    button_state_details = {
        FlashState.not_connected: ("( NO DEVICE PRESENT )"),
        FlashState.not_started: ( large(" Update {existing} to {version} ") ),
        FlashState.in_progress: ( large(" Updating {existing} to {version}") ),
        FlashState.error: ( large(" Aw, something bad happened...  ;-( ") ),
        FlashState.complete: ( large(" Update to {version} Complete "))
    }

    def __init__(self, **kwargs):
        super(ConnectedDevice, self).__init__(**kwargs)
        handler = FlashView(self)
        self.controller = create_threaded_controller(post_to_event_thread(handler))
        self.go.bind(on_release=lambda a:self.start())             # go button clicked
        self.device_changed()                                    # trigger first update

    def on_update_state(self, instance, value):
        state = self.update_state
        self.update_button()

    def on_device(self, instance, value):
        self.device_changed()

    def on_progress(self, instance, value):
        self.making_progress = True
        Clock.unschedule(self.inactivity)
        Clock.schedule_once(self.inactivity, 1) # flag inactivity after 1 second

    def inactivity(self, dt):
        self.making_progress = False

    def device_changed(self):
        opacity = 1.0 if self.device else 0.2
        anim = Animation(device_opacity=opacity, duration=0.25)
        anim.start(self)
        self.text = "Connected" if self.device else "Disconnected"
        self.update_button()

    def on_update_version(self, instance, value):
        self.update_button()

    """
    updates the button text to reflect the current state
    """
    def update_button(self):
        text = self.button_state_details.get(self.update_state).format(version=self.update_version)
        self.making_progress = True
        self.go_text = text

    def update(self, item):
        """Notification from the ConnectedDeviceModel"""
        self.device = item

    def start(self):
        connected = self.device
        if connected:
            self.controller.flash(connected)


class FlashView(UpdaterEvents):
    def __init__(self, root:ConnectedDevice):
        self.root = root

    def updater_state_changed(self, state:FlashState):
        print(threading.current_thread().name+" state changed to "+str(state))
        self.root.update_state = state

    def connected_device_changed(self, device):
        print(threading.current_thread().name+" device connected" if device else "device disconnected")
        self.root.device = device

    def error(self, error):
        print(error)

    def progress(self, min, max, current):
        self.root.progress = (current-min) / (max-min)


class Gui(App):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    """
    Manages the View and View Model. Changes to the view model
    """
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.title = "Particle Device Updater"
        self.icon = "resources/particle.png"
        self.thread = threading.current_thread()
        return ConnectedDevice()

    def on_pause(self):
        return True


def setup_working_dir():
    # This is needed to set the current working folder when extracting from a single executable
    if hasattr(sys, '_MEIPASS'):
        p = os.path.join(sys._MEIPASS)
        os.chdir(p)
        print("changed folder to "+p)


if __name__ == '__main__':
    setup_working_dir()
    Gui().run()
