from threading import Thread
from time import sleep

from PySimpleGUI import Window, WIN_CLOSED, Button, theme

IMAGE_O = 'assets/o.png'
IMAGE_X = 'assets/x.png'


class Task:
    def __init__(self, func):
        self.func = func
        self.args = ()
        self.kwargs = {}

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)

    def __str__(self):
        return str(self.args) + str(self.kwargs)


class TicTacToeGUI:
    @staticmethod
    def init_layout():
        layout = [[Button(size=(10, 5), key=f'{i}-{j}') for i in range(3)] for j in range(3)]
        return layout

    def __init__(self):
        self._running = False
        self._window = Window('TicTacToe', self.init_layout())
        self._tasks = []

    def is_running(self):
        return self._running

    def _work(self):
        while self._running is True:
            event, values = self._window.read()

            if event == WIN_CLOSED:
                self._running = False

            while len(self._tasks) > 0:
                self._tasks.pop().run()

    def start(self):
        if self._running is True:
            raise RuntimeError('Cannot run one window twice')

        self._running = True
        Thread(target=self._work, daemon=True).start()

    def set(self, x: int, y: int, color: str):

        if color in ['o', 'x']:
            self.add_task(self._window['-'.join((str(x), str(y)))].update)(
                image_filename=IMAGE_O if color == 'o' else IMAGE_X)

        else:
            raise ValueError("'color' must be 'o' or 'x")

    def add_task(self, task):
        task = Task(task)
        self._tasks.append(task)
        return task


if __name__ == '__main__':
    theme('black')
    t = TicTacToeGUI()
    t.start()
    t.set(0, 0, 'x')
    t.set(0, 1, 'o')

    while t.is_running():
        sleep(1)
