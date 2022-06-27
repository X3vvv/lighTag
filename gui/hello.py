from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty

from kivy.lang import Builder

Builder.load_file("hello.kv")  # explicitly assign the kv file with random name


class MyLayout(GridLayout):
    pass


class AwesomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    AwesomeApp().run()
