from typing import Tuple
from random import random

from kivy.config import Config

Config.read("./gui/lighTag/config.ini")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics import Line, Color, Ellipse
from kivy.lang.builder import Builder

Builder.load_file("main.kv")

# tag-base distances and postion of tag
tagBaseDist = [
    random() * 6.5 + 0.5,
    random() * 6.5 + 0.5,
    random() * 6.5 + 0.5,
    random() * 6.5 + 0.5,
]  # old name: inDisArr
tagPos = [random() * 4.5, random() * 4.5, random() * 2]  # old name: tri


def iot_callback(duration_after_last_call):
    global tagBaseDist, tagPos

    # mimic distance between tag and bases is changing
    for i in range(len(tagBaseDist)):
        tagBaseDist[i] += random() - 0.5

    # mimic tag's coords change
    for i in range(2):  # only change x & y coords, leave height
        tagPos[i] += random() - 0.2


Clock.schedule_interval(iot_callback, 0.5)
print("Kivy clock callback added.")


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

    tmp_pos = [120, 240]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def settings_on(self):
        """Not used yet."""
        self.ids.settings_img.source = "imgs/settings-outline-pressed.png"
        # self.ids.settings_btn.background_color = (0, 0, 0, 0)

    def settings_off(self):
        """Not used yet."""
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
            pos=(
                0,
                self.ids.control_panel.height,
            ),  # pos of left-bottom corner of the button
            on_release=self._on_base_released,
        )
        self.bases.append(new_base)
        self.ids.canvas.add_widget(new_base)  # add widget to the canvas widget
        self.num_of_base += 1

    def _on_base_released(self, base_btn):
        """Callback function for when the base button is released. A popup window will be created."""

        def popup_confirm(confirm_btn):
            """Callback function of confirm button in the base popup window."""
            # print(confirm_btn)
            x = y = z = 0
            if base_x.text.isdigit():
                x = float(base_x.text)
            if base_y.text.isdigit():
                y = float(base_y.text)
            if base_z.text.isdigit():
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
            base_btn.pos = [x, y + self.ids.control_panel.height]
            self.ids.canvas.remove_widget(popup)

        def delete_base(delete_btn):
            """Callback function of delete button in the base popup window."""
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

        # main layout of the popup window
        mainLayout = BoxLayout(orientation="vertical")

        # layout which holds all the position information
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

        # add confirm button
        mainLayout.add_widget(
            Button(text="Confirm", size_hint=(1, 0.45), on_release=popup_confirm)
        )

        # add delete button
        mainLayout.add_widget(
            Button(
                text="Delete",
                size_hint=(1, 0.45),
                color=(1, 30 / 255, 30 / 255, 1),
                on_release=delete_base,
                disabled=True,
            )
        )

        # add main layout to the popup window
        popup = Popup(
            title="Settings",
            content=mainLayout,
            size_hint=(None, None),
            size=(250, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.5},  # center of father widget
        )

        # add popup to the canvas
        self.ids.canvas.add_widget(popup)

    def debug(self):
        global tagBaseDist, tagPos

        # DEBUG: print base position of the window
        if len(self.bases) <= 0:
            print("No base yet.")
        else:
            for i in range(len(self.bases)):
                print("[base {}] pos on window: {}]".format(i, self.bases[i].pos))

        # DEBUG: print tagBaseDist & tagPos
        print("Tag-base distances:\n\t {}\n\t {}\n\t {}\n\t {}".format(*tagBaseDist))
        print("Tag location: {}".format(tagPos))

        # print a circle at the tag location
        print("Draw a circle at: ({}, {})...", tagPos[0], tagPos[1])
        self.draw_a_circle(tagPos[0], tagPos[1])
        print("Finish drawing!")

        # change tag-base distance labels
        self.update_tag_base_dist()

    def update_tag_base_dist(self):
        global tagBaseDist, tagPos
        self.ids.tag_distance.text = "Tag distance (m)\nbase1:  {:.2f}\nbase2:  {:.2f}\nbase3:  {:.2f}\nbase4:  {:.2f}".format(
            *tagBaseDist
        )

    def draw_a_circle(self, x, y, d=5):
        """
        Plot a circle on the canvas.
        #Param
        x: x-coords of the circle on the canvas
        y: y-coords of the circle on the canvas
        r: diameter of the circle
        """
        with self.ids.canvas.canvas:
            Color(0.9, 0.1, 0.1, 0.9)
            Ellipse(pos=(x, y + self.ids.canvas.height), size=(d, d))


class UIApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    UIApp().run()
