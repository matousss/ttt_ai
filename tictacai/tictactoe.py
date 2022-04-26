from copy import deepcopy
from threading import Thread

from PySimpleGUI import WIN_CLOSED, Window, Button

STONES = ('○', '⨉')
btn_size = (10, 5)


class TicTacToe:
    def __init__(self):
        self._stones = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
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

        return False


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

    @staticmethod
    def _get_symbol(_id: int):
        if _id == -1:
            return ''
        return STONES[_id]

    def _update_symbols(self):
        for row in range(3):
            for col in range(3):
                stone = self._stones[col][row]
                self._window[f'{row}-{col}'].update(text=self._get_symbol(stone), disabled=(stone != -1))

    def on_event(self, event, values):
        pass

    def _work(self):
        while self._running is True:
            event, values = self._window.read()
            if event == WIN_CLOSED:
                self._running = False
                return
            self.on_event(event, values)
            self._update_symbols()

    def start(self):
        if self._running is True:
            raise RuntimeError('Cannot run one window twice')

        self._running = True
        Thread(target=self._work, daemon=True).start()
