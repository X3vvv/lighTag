from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from kivy.lang import Builder

# explicitly assign the kv design file with random name
Builder.load_file("hello.kv")


class MyLayout(GridLayout):
    pass


class AwesomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    AwesomeApp().run()
