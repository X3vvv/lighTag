from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_string(
    """
<MainLayout>
    Label:
        text: "hello world"
"""
)


def f():
    print(123)


Clock.schedule_interval(f, 1)


class MainLayout(Widget):
    pass


class TestApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    TestApp().run()
