from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder


Builder.load_file("main.kv")


class MainLayout(Widget):
    pass


class MainApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MainApp().run()
