from copy import deepcopy
from threading import Thread

from PySimpleGUI import WIN_CLOSED, Window, Button

from tictactoe.players import Player
from tictactoe.util import STONE_STR, STONES_BASE64, Stone, GameState, get_default_desk, _default_chooser, check_win


# Class represents a game of TicTacToe
class TicTacToe:
    def __init__(self, player1, player2, *, choose_next_player=_default_chooser, max_games=None):
        self._stones = get_default_desk()
        self.players = (player1, player2)
        self._last_played = None
        self._max_games = max_games
        self._game_num = 0
        self._draws = 0

        # init players
        for p in self.players:
            p.set_game(self)

        self.choose_next_player = choose_next_player
        self._player_on_roll = self.choose_next_player(self)

    def get_player_on_roll(self) -> Player:
        return self.players[self._player_on_roll]

    def next_roll(self):
        self.get_player_on_roll().on_roll()

    def set_stone(self, x, y, stone):
        self._stones[x][y] = stone

    def _notify_end(self, game_state):
        for p in self.players:
            p.game_over(game_state)

    def _game_over(self, game_state):
        print(f'Game ended: {"draw" if game_state == GameState.DRAW else f"{STONE_STR[game_state]} wins"}')
        self._game_num += 1
        if game_state == GameState.DRAW:
            self._draws += 1
        if self._game_num == self._max_games:
            return
        self._notify_end(game_state)
        self._player_on_roll = self.choose_next_player(self)
        self._stones = get_default_desk()

        self.next_roll()

    """
    Places a stone on the desk.
    :param x: x coordinate of the stone
    :param y: y coordinate of the stone
    """
    def play(self, x, y):
        if self._stones[x][y] != Stone.EMPTY:
            raise ValueError('This cell is already occupied')

        self.set_stone(x, y, self.get_player_on_roll().color)

        game_state = check_win(self._stones)
        if game_state != -1:
            self._game_over(game_state)

        else:
            self._last_played = self._player_on_roll
            self._player_on_roll = Stone.O_PLAYER if self._player_on_roll == Stone.X_PLAYER else Stone.X_PLAYER

    """
    Returns copy of current desk state
    """
    def get_desk(self):
        return deepcopy(self._stones)

    def start(self):
        self.next_roll()

    def get_scores(self):
        return self._game_num, self._draws, self.players[0].score, self.players[1].score

    def start(self):
        while True:
            self.next_roll()
            if self._game_num == self._max_games:
                break

#
#
#
#
#
#
#
#
# Game representation with GUI
class TicTacToeGUI(TicTacToe):
    BTN_SIZE = 120, 120

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

    """
    Check if game window is running
    """
    def is_running(self):
        return self._running

    @staticmethod
    def _get_symbol(_id: int):
        val = {
            'image_data': '',
            'image_size': TicTacToeGUI.BTN_SIZE,
        }
        if _id == Stone.EMPTY:
            return val

        val['image_data'] = STONES_BASE64[_id]

        return val

    def _update_symbols(self):
        for col in range(3):
            for row in range(3):
                stone = self._stones[col][row]
                self._window[f'{row}-{col}'].update(disabled=(stone != -1), **self._get_symbol(stone))

    def play(self, x, y):
        super().play(x, y)
        self._update_symbols()

    def on_event(self, *args, **kwargs):
        self.get_player_on_roll().on_event(*args, **kwargs)

    def _fix_btns(self):
        self._window.read(timeout=1)
        self._update_symbols()

    def _work(self):
        self._fix_btns()
        while self._running is True:
            if self._game_num == self._max_games:
                self._running = False
                break
            event, values = self._window.read(timeout=100)
            if event == WIN_CLOSED:
                self._running = False
                return
            self.on_event(event, values)
            if self._last_played is not self.get_player_on_roll().color:
                self.next_roll()

    def start(self):
        if self._running is True:
            raise RuntimeError('Cannot run one window twice')

        self._running = True
        self._work()
