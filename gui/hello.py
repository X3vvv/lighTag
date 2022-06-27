from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty

from kivy.lang import Builder

# Builder.load_file("randomname.kv")  # explicitly assign the kv file with random name
Builder.load_string(
    """
<MyGridLayout>

    name: username  # object: id
    pwd: password  # object: id

    GridLayout:
        cols: 1
        size: root.width, root.height

        GridLayout:
            cols: 2

            Label:
                text: "Username"
            TextInput:
                id: username
                multiline: False

            Label:
                text: "Password"
            TextInput:
                id: password
                multiline: False
                password: True

        Button:
            text: "Submit"
            font_size: 32
            on_press: root.press()
"""
)


class MyGridLayout(GridLayout):

    name = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def press(self):
        # Function of the submit button
        name = self.name.text
        pwd = self.pwd.text

        # print("Hello {}, your password is: {}".format(name, pwd))

        # Print info to screen
        if name.strip() == "" or pwd.strip() == "":
            msg = "Error: must fill the username and password"
        else:
            msg = "Hello {}, your password is: {}".format(name, pwd)
            # Clear the input boxes
            self.name.text = ""
            self.pwd.text = ""
        self.add_widget(Label(text=msg))


class AwesomeApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == "__main__":
    AwesomeApp().run()
