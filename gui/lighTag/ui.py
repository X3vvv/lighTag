from random import random

from kivy.config import Config

import backend

Config.read("./gui/lighTag/config.ini")

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

# from kivy.lang.builder import Builder
# Builder.load_file("ui.kv")

DEBUG_UI = True  # if True, won't connect backend, run simulation data instead


class Base:
    SIDE_LEN = 17  # side length of the squred base button
    FONT_SIZE = 13  # font size of the text on the button
    CANVAS_ORIGIN_OFFSET = (0, 250)  # canvas origin's position relative to the window

    # no class variable is defined

    def __init__(self, id, father_widget):
        """
        Instance variables (values differs in different instances):
            self.id: base id
            self.widget: kivy button widget
            self.father_widget: kivy father widget of the base button
            self.x = y = z: position of the base button on the canvas
        """
        self.id = id

        # init base position on the canvas
        self.x = 0
        self.y = 0
        self.z = 0

        # create the button
        self.widget = self.create_button()
        # father widget
        self.father_widget = father_widget

    def update_pos(self, x, y, z=None):
        """Update button position fields values and window position."""
        # update fields
        self.x = x
        self.y = y
        if z is not None:
            self.z = z

        # update widget on window
        self.widget.pos = (x, y)

    def get_pos_on_window(self):
        """Return the position of the base button on the whole 2D window."""
        return (
            self.x + self.CANVAS_ORIGIN_OFFSET[0],
            self.y + self.CANVAS_ORIGIN_OFFSET[1],
        )

    def create_button(self):
        btn = Button(
            text=str(self.id),
            font_size=self.FONT_SIZE,
            size_hint=(None, None),
            size=(self.SIDE_LEN, self.SIDE_LEN),
            pos=self.get_pos_on_window(),
            on_release=self._on_button_released,
        )
        self.id += 1
        return btn

    def _on_button_released(self):
        """Callback function for when the base button is released. A popup window will be created."""

        def create_popup_window(self):
            """Create a popup window for the base button."""

            def popup_confirm(confirm_btn):
                """Callback function of confirm button in the base popup window. If the input isn't number, set to 0 by default."""
                x = y = z = 0
                if base_x.text.isdigit():
                    x = float(base_x.text)
                if base_y.text.isdigit():
                    y = float(base_y.text)
                if base_z.text.isdigit():
                    z = float(base_z.text)
                if x < 0:
                    x = 0
                elif x > self.ids.canvas_temp_label.size[0] - 17:
                    x = self.ids.canvas_temp_label.size[0] - 17
                if y < 0:
                    y = 0
                elif y > self.ids.canvas_temp_label.size[1] - 17:
                    y = self.ids.canvas_temp_label.size[1] - 17
                self.widget.pos = [x, y + self.father_widget.ids.control_panel.height]
                self.father_widget.ids.canvas.remove_widget(popup)

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
            return Popup(
                title="Settings",
                content=mainLayout,
                size_hint=(None, None),
                size=(250, 200),
                pos_hint={"center_x": 0.5, "center_y": 0.5},  # center of father widget
            )

        popup = create_popup_window()
        self.ids.canvas.add_widget(popup)


class MainLayout(Widget):
    num_of_base = 0
    focused_base = None
    bases = []
    CENTIMETER_PER_PIXEL = 1.5  # how many centimeters a kivy pixel represents

    draw_path_has_started = False
    draw_path_event = None

    FIRST_FLOOR_CELLING_HEIGHT = 1.5
    FLOOR_COLORS = {
        "default": (0.9, 0.1, 0.1, 0.9),
        "1": (101 / 255, 9 / 255, 179 / 255, 1),
        "2": (0 / 255, 166 / 255, 66 / 255, 1),
    }
    path_dot_color = None  # color of the dot used to draw the path

    PATH_DOT_DIAMETER_IN_PIXEL = 10
    REVERSE_XY = True  # reverse x-y axis
    CLOCK_SCHEDULE_INTERVAL = 1  # interval of the callbacks added to the clock

    alive_path_dot_list = []  # stores a list of (color, circle) tuples
    PATH_DOT_LIFETIME = 8  # (unit: update time) each path dot's life time, old dots will gradually fade out and be removed from the alive_path_dot_list lise

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tagPos = [-1, -1, -1]
        self.tagBaseDist = [-1, -1, -1, -1]

        self.start_backend()
        Clock.schedule_interval(
            lambda dt: self.update_tag_data(), self.CLOCK_SCHEDULE_INTERVAL
        )

    def start_backend(self):
        if DEBUG_UI:
            self.tagPos = [2, 2, 2]
            self.tagBaseDist = [7.777, 7.777, 7.777, 7.777]

            def gen_simulate_data():
                # simulate tagPos change
                xy_delta = 1
                z_delta = 1
                self.tagPos[0] += random() * xy_delta - xy_delta / 2
                self.tagPos[1] += random() * xy_delta - xy_delta / 2
                self.tagPos[2] += random() * z_delta - z_delta / 2

                # simulate tagBaseDist change
                dist_delta = 1
                for i in range(len(self.tagBaseDist)):
                    self.tagBaseDist[i] += random() * dist_delta - dist_delta / 2

            Clock.schedule_interval(
                lambda dt: gen_simulate_data(), self.CLOCK_SCHEDULE_INTERVAL
            )

        else:
            lt = backend.lighTagAlgo()
            lt.wifiConnect()
            lt.setBaseACoor(0, 0, 2.0)
            lt.setBaseBCoor(0, 8.535, 2.0)
            lt.setBaseCCoor(5.86, 8.535, 2.0)
            lt.setBaseDCoor(5.86, 0.0, 2.355)
            Clock.schedule_interval(lambda dt: lt.run(), self.CLOCK_SCHEDULE_INTERVAL)
            self.lt = lt
        print("Starting backend")

    def update_tag_data(self):
        """Update text of tag-base distances label on the window."""
        if DEBUG_UI:
            self.tagBaseDist = self.tagBaseDist
            self.tagPos = self.tagPos
        else:
            self.tagBaseDist = self.lt.getDistance()
            self.tagPos = self.lt.getCoor()

        if self.REVERSE_XY:
            self.tagPos[0], self.tagPos[1] = self.tagPos[1], self.tagPos[0]

        # edge fix
        for i in range(len(self.tagPos)):
            if self.tagPos[i] < 0:
                self.tagPos[i] = 0

        # update tag_distance label
        self.ids.tag_distance.text = "Tag info (m)\nbase1:  {:.2f}\nbase2:  {:.2f}\nbase3:  {:.2f}\nbase4:  {:.2f}\n\n(x:{:.1f}, y:{:.1f}, h:{:.1f})".format(
            *self.tagBaseDist, *self.tagPos
        )

        # update floor label
        floor = "1" if self.tagPos[2] < self.FIRST_FLOOR_CELLING_HEIGHT else "2"
        self.ids.floor_label.text = f"Floor: {floor} L"

        # update colors of floor label & path dots
        self.path_dot_color = self._get_floor_color(floor)
        self.ids.floor_label.color = self._get_floor_color(floor)

        # DEBUG: print tag information
        print(
            "Tag: x={:.1f}m, y={:.1f}m, h={:.1f}m [({:.1f}, {:.1f}) pixel]".format(
                *self.tagPos, *self.get_tag_pixel_pos()[:2]
            )
        )

    def _get_floor_color(self, floor: str):
        return (
            self.FLOOR_COLORS[floor]
            if floor in self.FLOOR_COLORS.keys()
            else self.FLOOR_COLORS["default"]
        )

    def _on_settings_pressed(self):
        """Not used yet."""
        # self.ids.settings_btn.background_color = (0, 0, 0, 0)
        self.ids.settings_img.source = "imgs/settings-outline-pressed.png"

    def on_settings_released(self):
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
        # print global positions of all the bases
        print("========= DEBUG messages =========")
        print("Base details:")
        if len(self.bases) <= 0:
            print("\tNo base yet.")
        else:
            for i in range(len(self.bases)):
                print("\t[base {}] pos on window: {}]".format(i, self.bases[i].pos))
        print()

        # print all drawed circles
        print("Canvas instructions details:")
        for color, circle in self.alive_path_dot_list:
            print("\t{}\n\t{}\n".format(color, circle))
        print()

    def on_plot_path_released(self):
        def draw_path_callback(duration_after_last_call):
            self.draw_a_circle(*self.get_tag_pixel_pos()[:2])
            self.update_path_dots_transparency()

        if self.draw_path_has_started:  # IS drawing path, will stop drawing
            if self.draw_path_event is None:
                raise ValueError(
                    "draw_path_event is supposed to be a event but None value is detected."
                )
            self.draw_path_event.cancel()
            self.draw_path_has_started = False
            # print("-- Draw path event has been cancelled")
            self.ids.start_plotting_path_btn.text = "START plotting path"
        else:  # is NOT drawing path, will start drawing
            self.draw_path_event = Clock.schedule_interval(draw_path_callback, 1)
            self.draw_path_has_started = True
            # print("-- Draw path event has started")
            self.ids.start_plotting_path_btn.text = "STOP plotting path"

    def draw_a_circle(self, x, y):
        """
        Plot a circle on the canvas.
        #Param
        x: x-coords of the circle on the canvas
        y: y-coords of the circle on the canvas
        r: diameter of the circle
        """
        # print("Draw a circle at: [{}, {}]".format(x, y))
        color = self.path_dot_color or (0.9, 0.1, 0.1, 0.9)

        # canvas add new color and circle
        new_path_dot_color = Color(*color)
        new_path_dot = Ellipse(
            pos=(x, y + self.ids.control_panel.height),
            size=(self.PATH_DOT_DIAMETER_IN_PIXEL, self.PATH_DOT_DIAMETER_IN_PIXEL),
        )
        self.ids.canvas.canvas.add(new_path_dot_color)
        self.ids.canvas.canvas.add(new_path_dot)

        # add circle to alive path dot list
        self.alive_path_dot_list.append((new_path_dot_color, new_path_dot))

        # # draw a circle onto the canvas
        # with self.ids.canvas.canvas:
        #     Color(*color)
        #     Ellipse(
        #         pos=(x, y + self.ids.control_panel.height),
        #         size=(self.PATH_DOT_DIAMETER_IN_PIXEL, self.PATH_DOT_DIAMETER_IN_PIXEL),
        #     )
        pass

    def update_path_dots_transparency(self):
        to_be_deleted_dot_idx_list = []
        for i in range(len(self.alive_path_dot_list)):
            curr_circle_color = self.alive_path_dot_list[i][0]
            if curr_circle_color.a <= 0:
                to_be_deleted_dot_idx_list.append(i)
            else:
                curr_circle_color.a -= 1 / self.PATH_DOT_LIFETIME

        while len(to_be_deleted_dot_idx_list) > 0:
            del self.alive_path_dot_list[to_be_deleted_dot_idx_list.pop()]

        # print("to_be_deleted_dot_idx_list:\n\t", to_be_deleted_dot_idx_list)
        # print("len(self.alive_path_dot_list):\n\t", len(self.alive_path_dot_list))

    def get_tag_pixel_pos(self):
        """Get tag position in pixel (unit: meter -> pixel)."""
        tmp = self.tagPos.copy()
        for i in range(len(tmp)):
            tmp[i] = tmp[i] * 100 / self.CENTIMETER_PER_PIXEL  # m * cm/m / cm/px
        return tmp


class UIApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    UIApp().run()
