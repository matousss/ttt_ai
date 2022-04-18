from kivy.app import App
from kivy.uix.widget import Widget


class Desk(Widget):
    pass


class TTTApp(App):
    def build(self):
        return Desk()


if __name__ == '__main__':
    TTTApp().run()
