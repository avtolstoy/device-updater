from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button

#Config.set('graphics', 'fullscreen', 'fake')

class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()
