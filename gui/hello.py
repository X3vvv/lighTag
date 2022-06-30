from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

from kivy.core.window import Window

# explicitly assign the kv design file with random name
Builder.load_file("hello.kv")


class MyLayout(Widget):
    pass


class AwesomeApp(App):
    def build(self):
        Window.clearcolor = (
            0.2,
            0.1,
            0.4,
            1,
        )  # can be overwrite by kv design file's setting
        return MyLayout()


if __name__ == "__main__":
    AwesomeApp().run()
