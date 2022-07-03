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


class MainLayout(Widget):
    def settings_on(self):
        self.ids.settings_img.source = "imgs/settings-outline-pressed.png"
        # self.ids.settings_btn.background_color = (0, 0, 0, 0)

    def settings_off(self):
        self.ids.settings_img.source = "imgs/settings-outline.png"


class MainApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MainApp().run()
