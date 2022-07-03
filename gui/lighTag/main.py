from tkinter import N
from kivy import Config

# set default window size and minumum size
Config.set("graphics", "width", "450")
Config.set("graphics", "height", "750")
Config.set("graphics", "minimum_width", "450")
Config.set("graphics", "minimum_height", "750")

from kivy.lang import Builder

# load kivy design file
Builder.load_file("main.kv")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class MainLayout(Widget):
    num_of_base = 0

    def settings_on(self):
        self.ids.settings_img.source = "imgs/settings-outline-pressed.png"
        # self.ids.settings_btn.background_color = (0, 0, 0, 0)

    def settings_off(self):
        self.ids.settings_img.source = "imgs/settings-outline.png"

    def add_base(self):
        base_id = self.num_of_base + 1
        new_base = self._create_base(base_id)
        canvas = self.ids.canvas
        canvas.add_widget(new_base)
        self.num_of_base += 1

    def _create_base_popup(self):
        def popup_confirm(not_used):
            # print(not_used)  # the button
            x = base_x.text
            y = base_y.text
            z = base_z.text
            print(x, y, z)
            self.ids.canvas.remove_widget(popup)

        mainLayout = BoxLayout(orientation="vertical")

        posLayout = GridLayout(cols=2)
        base_x = TextInput(multiline=False)
        base_y = TextInput(multiline=False)
        base_z = TextInput(multiline=False)
        posLayout.add_widget(Label(text="x:"))
        posLayout.add_widget(base_x)
        posLayout.add_widget(Label(text="y:"))
        posLayout.add_widget(base_y)
        posLayout.add_widget(Label(text="z:"))
        posLayout.add_widget(base_z)

        mainLayout.add_widget(posLayout)
        mainLayout.add_widget(Button(text="Confirm", on_release=popup_confirm))

        popup = Popup(
            title="Settings",
            content=mainLayout,
            size_hint=(None, None),
            size=(250, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        return popup

    def _base_add_popup(self, not_used):
        # print(not_used)  # the button object
        self.ids.canvas.add_widget(self._create_base_popup())

    def _create_base(self, id):
        return Button(
            text=str(id),
            size_hint=(None, None),
            size=(10, 10),
            pos_hint={"x": 0.5, "y": 0.5},
            on_release=self._base_add_popup,
        )


class MainApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MainApp().run()
