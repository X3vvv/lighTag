from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

# explicitly assign the kv design file with random name
Builder.load_file("hello.kv")


class MyLayout(Widget):
    pass


class AwesomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    AwesomeApp().run()
