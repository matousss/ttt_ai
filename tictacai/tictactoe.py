from copy import deepcopy
import random
from threading import Thread

from PySimpleGUI import WIN_CLOSED, Window, Button

from tictacai.players import Player

STONES = ('○', '⨉')
btn_size = (10, 5)

_default_desk = [
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
]


class TicTacToe:
    def __init__(self, player1, player2):
        self._stones = deepcopy(_default_desk)

        self.players = (player1, player2)
        for p in self.players:
            p.set_desk(self)
        self._player_on_roll = random.randint(0, 1)

    def get_player_on_roll(self) -> Player:
        return self.players[self._player_on_roll]

    def next_roll(self):
        self.get_player_on_roll().on_roll()

    def set_stone(self, x, y, stone):
        self._stones[x][y] = stone

    def play(self, x, y):
        self.set_stone(x, y, self.get_player_on_roll().color)

        game_state = self.check_win()
        if game_state != -1:
            print(f'end game: {STONES[self.check_win()]}')

            for p in self.players:
                p.game_over(game_state)
            self._stones = deepcopy(_default_desk)
            # todo

        self._player_on_roll = 1 if self._player_on_roll == 0 else 0
        print(self._player_on_roll)
        self.next_roll()

    def get_desk(self):
        return deepcopy(self._stones)

    def check_win(self):
        for i in range(3):
            a = self._stones[i][0]
            if a == -1:
                continue
            for j in range(1, 3):
                if self._stones[i][j] != a:
                    break
            else:
                return a

        for i in range(3):
            a = self._stones[0][i]
            if a == -1:
                continue
            for j in range(1, 3):
                if self._stones[j][i] != a:
                    break
            else:
                return a

        for i in range(2):
            a = self._stones[i * 2][0]
            if a == -1:
                continue
            for j in range(1, 3):

                if self._stones[abs(i * 2 - j)][j] != a:
                    break

            else:
                return a

        return -1


class TicTacToeGUI(TicTacToe):
    @staticmethod
    def init_layout():
        layout = [[Button(size=btn_size, key=f'{i}-{j}', font=('Arial', 30)) for i in range(3)] for j in range(3)]
        return layout

    def __init__(self, *args):
        super().__init__(*args)
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

    def on_event(self, *args, **kwargs):
        self.get_player_on_roll().on_event(*args, **kwargs)

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
