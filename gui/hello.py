from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

# explicitly assign the kv design file with random name
Builder.load_file("hello.kv")


class MyLayout(Widget):
    def press(self):
        # create variables for the widget
        name = self.ids.nameInput.text
        # print(name)

        # update the label
        self.ids.nameLabel.text = f"Hello {name}!"
        self.ids.nameInput.text = ""
        self.ids.submitButton.text = "Quit"


class AwesomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    AwesomeApp().run()
