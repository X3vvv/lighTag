from faulthandler import disable
from typing import Tuple

from kivy import Config

# set default window size and minumum size
Config.set("graphics", "width", "450")
Config.set("graphics", "height", "750")
Config.set("graphics", "minimum_width", "450")
Config.set("graphics", "minimum_height", "750")

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class Base:
    SIDE_LEN = 17
    FONT_SIZE = 13
    CANVAS_ORIGIN_OFFSET = (0, 250)  # canvas origin's position relative to the window

    def __init__(self, id):
        self.id = id

        # init base position: default at (0, 0) (which is actually (0, 0) + CANVAS_ORIGIN_OFFSET on window)
        self.x = 0
        self.y = 0
        self.z = 0

        self.pos_on_screen = self.move_pos((self.x, self.y), self.CANVAS_ORIGIN_OFFSET)

        self.widget = Button(
            text=str(self.id),
            font_size=self.FONT_SIZE,
            size_hint=(None, None),
            size=(self.SIDE_LEN, self.SIDE_LEN),
            pos=self.pos_on_screen,
            on_release=self._on_add_base_released,
        )

    def move_pos(self, ori_pos: Tuple[float, float], move_dist: Tuple[float, float]):
        return (ori_pos[0] + move_dist[0], ori_pos[1] + move_dist[1])

    def update_pos(self, new_pos):
        self.pos_on_screen = new_pos
        self.widget.pos = self.pos_on_screen


class MainLayout(Widget):
    num_of_base = 0
    focused_base = None
    bases = []
    CENTIMETER_PER_PIXEL = 1  # how many centimeters a kivy pixel represents

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def settings_on(self):
        self.ids.settings_img.source = "imgs/settings-outline-pressed.png"
        # self.ids.settings_btn.background_color = (0, 0, 0, 0)

    def settings_off(self):
        self.ids.settings_img.source = "imgs/settings-outline.png"

    def add_base(self):
        """Callback function for adding a base button to the canvas."""
        base_id = self.num_of_base + 1
        new_base = Button(
            text=str(base_id),
            font_size=13,
            size_hint=(None, None),
            size=(17, 17),
            # pos_hint={"x": 0.5, "y": 0.5},
            pos=(0, 250),  # pos of left-bottom corner of the button
            on_release=self._on_base_released,
        )
        self.bases.append(new_base)
        canvas = self.ids.canvas
        canvas.add_widget(new_base)
        self.num_of_base += 1

    def _on_base_released(self, base_btn):
        """Callback function for when the base button is released. A popup window will be created."""

        def popup_confirm(confirm_btn):
            # print(confirm_btn)
            x = float(base_x.text)
            y = float(base_y.text)
            z = float(base_z.text)
            print(x, y, z)
            if x < 0:
                x = 0
            elif x > self.ids.canvas_temp_label.size[0] - 17:
                x = self.ids.canvas_temp_label.size[0] - 17
            if y < 0:
                y = 0
            elif y > self.ids.canvas_temp_label.size[1] - 17:
                y = self.ids.canvas_temp_label.size[1] - 17
            base_btn.pos = [x, y + 250]
            self.ids.canvas.remove_widget(popup)

        def delete_base(delete_btn):
            # def confirm_delete_base(confirm_delete_btn):
            #     self.ids.canvas.remove_widget(doubleCheckPopup)

            # def cancel_delete_base(cancel_delete_btn):
            #     self.ids.canvas.remove_widget(doubleCheckPopup)

            # doubleCheckLayout = BoxLayout(orientation="vertical")
            # doubleCheckLayout.add_widget(
            #     Label(text="Are you sure to delete this base?", font_size=20)
            # )
            # doubleCheckLayout.add_widget(
            #     Button(text="Yes", size_hint=(1, 0.4), on_release=confirm_delete_base)
            # )
            # doubleCheckLayout.add_widget(
            #     Button(text="Cancel", size_hint=(1, 0.4), on_release=cancel_delete_base)
            # )
            # doubleCheckPopup = Popup(
            #     title="Settings",
            #     content=doubleCheckLayout,
            #     size_hint=(None, None),
            #     size=(200, 150),
            #     pos_hint={
            #         "center_x": 0.5,
            #         "center_y": 0.500,
            #     },
            # )
            # self.ids.canvas.add_widget(doubleCheckPopup)
            pass

        mainLayout = BoxLayout(orientation="vertical")

        posLayout = GridLayout(cols=2)
        base_x = TextInput(multiline=False, text="0", font_size=10)
        base_y = TextInput(multiline=False, text="0", font_size=10)
        base_z = TextInput(multiline=False, text="0", font_size=10)
        posLayout.add_widget(Label(text="x:"))
        posLayout.add_widget(base_x)
        posLayout.add_widget(Label(text="y:"))
        posLayout.add_widget(base_y)
        posLayout.add_widget(Label(text="z:"))
        posLayout.add_widget(base_z)

        mainLayout.add_widget(posLayout)
        mainLayout.add_widget(
            Button(text="Confirm", size_hint=(1, 0.45), on_release=popup_confirm)
        )
        mainLayout.add_widget(
            Button(
                text="Delete",
                size_hint=(1, 0.45),
                color=(1, 30 / 255, 30 / 255, 1),
                on_release=delete_base,
                disabled=True,
            )
        )

        popup = Popup(
            title="Settings",
            content=mainLayout,
            size_hint=(None, None),
            size=(250, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.ids.canvas.add_widget(popup)

    def debug(self):
        for i in range(len(self.bases)):
            print("base[{}]: {}]".format(i, self.bases[i].pos))
        if len(self.bases) <= 0:
            print("No base yet.")

    def update_label_dist(self, arr):
        print(arr)

    def update_label_pos(self, arr):
        print(arr)


def hello():
    print("Hello")


class UIApp(App):
    def build(self):
        self.main = MainLayout()
        return self.main


if __name__ == "__main__":
    UIApp().run()