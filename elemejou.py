import random
from copy import deepcopy
from threading import Thread
from time import sleep

from PySimpleGUI import Window, WIN_CLOSED, Button, theme


# IMAGE_O = 'assets/o.png'
# IMAGE_X = 'assets/x.png'


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


btn_size = (10, 5)


class TicTacToe:
    def __init__(self):
        self._stones = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def set_stone(self, x, y, stone):
        self._stones[x][y] = stone

    def get_desk(self):
        return deepcopy(self._stones)

    def check_win(self):
        for i in range(3):
            a = self._stones[i][0]
            if a == 0:
                continue
            for j in range(1, 3):
                if self._stones[i][j] != a:
                    break
            else:
                return True

        for i in range(3):
            a = self._stones[0][i]
            if a == 0:
                continue
            for j in range(1, 3):
                if self._stones[j][i] != a:
                    break
            else:
                return True








class TicTacToeGUI(TicTacToe):
    @staticmethod
    def init_layout():
        layout = [[Button(size=btn_size, key=f'{i}-{j}', font=('Arial', 30)) for i in range(3)] for j in range(3)]
        return layout

    def __init__(self):
        super().__init__()
        self._running = False
        self._window = Window('TicTacToe', self.init_layout())
        # self._tasks = []

    def is_running(self):
        return self._running

    def _get_symbol(self, _id: int):
        if _id == 0:
            return ''
        if _id == 1:
            return '○'
        if _id == 2:
            return '⨉'

    def _update_symbols(self):
        for row in range(3):
            for col in range(3):
                stone = self._stones[col][row]
                self._window[f'{row}-{col}'].update(text=self._get_symbol(stone), disabled=(stone != 0))

    def _work(self):
        while self._running is True:

            event, values = self._window.read(timeout=100)

            if event == WIN_CLOSED:
                self._running = False
                return

            self._update_symbols()

    def start(self):
        if self._running is True:
            raise RuntimeError('Cannot run one window twice')

        self._running = True
        Thread(target=self._work, daemon=True).start()


if __name__ == '__main__':
    theme('black')
    t = TicTacToeGUI()
    t.start()
    while t.is_running():
        sleep(.1)
        t.set_stone(random.randrange(0, 3), random.randrange(0, 3), random.randrange(1, 3))
        print(t.get_desk())
