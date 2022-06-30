from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

# explicitly assign the kv design file with random name
Builder.load_file("hello.kv")


class MyLayout(Widget):
    def press(self, content):
        print(content)


class AwesomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    AwesomeApp().run()
