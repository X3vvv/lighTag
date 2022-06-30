from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

# set the window size
Window.size = (500, 700)

# explicitly assign the kv design file with random name
Builder.load_file("hello.kv")


class MyLayout(Widget):

    current_action = ""

    def clear(self):
        self.ids.calcInput.text = "0"

    def button_press(self, button):
        content = self.ids.calcInput.text

        if content == "0":
            self.ids.calcInput.text = button
        else:
            self.ids.calcInput.text = content + button

    def add(self):
        content = self.ids.calcInput.text

        self.ids.calcInput.text += "+"


class AwesomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    AwesomeApp().run()
