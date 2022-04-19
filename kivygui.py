from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class TButton(Button):
    pass


class Desk(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        gl = GridLayout(cols=3, rows=3)
        for i in range(3):
            for j in range(3):
                gl.add_widget(Button(size_hint=(.6, .6)))

        self.add_widget(gl)


class TTTApp(App):
    def build(self):
        return Desk()


if __name__ == '__main__':
    TTTApp().run()
