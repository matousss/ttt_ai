import base64
from copy import deepcopy
import random
from threading import Thread

from PySimpleGUI import WIN_CLOSED, Window, Button

from tictactoe.players import Player

STONES = ('○', '⨉')
STONES_ASSETS = (
    './assets/o.png',
    './assets/x.png',
)


def convert_img_base64(src):
    with open(src, "rb") as img_file:
        return base64.b64encode(img_file.read())


STONES_BASE64 = [convert_img_base64(s) for s in STONES_ASSETS]

btn_size = (12, 6)

_DEFAULT_DESK = [
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
]


def _default_chooser(game: 'TicTacToe'):
    return random.randint(0, 1)


class TicTacToe:
    def __init__(self, player1, player2, *, choose_next_player=_default_chooser):
        self._stones = deepcopy(_DEFAULT_DESK)

        self.players = (player1, player2)
        for p in self.players:
            p.set_desk(self)

        self.choose_next_player = choose_next_player
        self._player_on_roll = self.choose_next_player(self)

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
            winner = self.check_win()
            print(f'end game: {"tie" if winner == 3 else STONES[winner]}')

            for p in self.players:
                p.game_over(game_state)
            self._stones = deepcopy(_DEFAULT_DESK)

            self._player_on_roll = self.choose_next_player(self)
            # todo

        else:
            self._player_on_roll = 1 if self._player_on_roll == 0 else 0

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

        for col in self._stones:
            for stone in col:
                if stone == -1:
                    return -1

        return 3


class TicTacToeGUI(TicTacToe):
    @staticmethod
    def init_layout():
        layout = [[
            Button(key=f'{i}-{j}', image_data='', border_width=0, disabled_button_color=('black', 'black'))
            for i in range(3)
        ] for j in range(3)]
        return layout

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._running = False
        self._window = Window('TicTacToe', self.init_layout())

    def is_running(self):
        return self._running

    @staticmethod
    def _get_symbol(_id: int):
        val = {
            'image_data': '',
            'image_size': (btn_size[0] * 10, btn_size[1] * 20),
        }
        if _id == -1:
            return val

        val['image_data'] = STONES_BASE64[_id]

        return val

    def _update_symbols(self):
        for row in range(3):
            for col in range(3):
                stone = self._stones[col][row]
                self._window[f'{row}-{col}'].update(disabled=(stone != -1), **self._get_symbol(stone))

    def on_event(self, *args, **kwargs):
        self.get_player_on_roll().on_event(*args, **kwargs)

    def _fix_btns(self):
        self._window.read(timeout=1)
        self._update_symbols()

    def _work(self):
        self._fix_btns()

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
