import kivy
from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class MyGridLayout(GridLayout):
    # Initialize infinite keywords
    def __init__(self, **kwargs):
        # Call grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 1

        # Create a second grid layout
        self.top_grid = GridLayout()
        self.top_grid.cols = 2

        # Add the second grid layout to the screen
        self.add_widget(self.top_grid)

        # Add username input box
        self.top_grid.add_widget(Label(text="Username: "))
        self.name = TextInput(multiline=False)
        self.top_grid.add_widget(self.name)

        # Add password input box
        self.top_grid.add_widget(Label(text="Password: "))
        self.pwd = TextInput(multiline=False, password=True)
        self.top_grid.add_widget(self.pwd)

        # Create submit button
        self.submit = Button(text="Submit", font_size=32)
        # Bind the button
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)

    def press(self, instance):
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


class MyApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == "__main__":
    MyApp().run()
