from copy import deepcopy
from threading import Thread
from time import sleep

from PySimpleGUI import WIN_CLOSED, Window, Button

from tictactoe.players import Player
from tictactoe.util import STONE_STR, STONES_BASE64, Stone, GameState, get_default_desk, _default_chooser, check_win


# Class represents a game of TicTacToe
class TicTacToe:
    def __init__(self, player_class1, player_class2, *, choose_next_player=_default_chooser, max_games=None):
        self._stones = get_default_desk()
        player1 = player_class1(Stone.X_PLAYER)
        player2 = player_class2(Stone.O_PLAYER)
        self.players = (player1, player2)
        self._color_to_player = {
            player1.color: player1,
            player2.color: player2,
        }
        self._roll_ended = True
        self._max_games = max_games
        self._game_num = 0
        self._draws = 0

        # init players
        for p in self.players:
            p.set_game(self)

        self.choose_next_player = choose_next_player
        self._player_on_roll = self.choose_next_player(self)

    def get_player_on_roll(self) -> Player:
        return self._color_to_player[self._player_on_roll]

    def next_roll(self):
        self.get_player_on_roll().on_roll()

    def set_stone(self, x, y, stone):
        self._stones[x][y] = stone

    def _notify_end(self, game_state):
        for p in self.players:
            p.game_over(game_state)

    def _print_winner(self, game_state):
        print(f'Game ended: {"draw" if game_state == GameState.DRAW else f"{STONE_STR[game_state]} wins"}')

    def _restart(self):
        self._player_on_roll = self.choose_next_player(self)
        self._stones = get_default_desk()
        self._roll_ended = True

    def _game_over(self, game_state):
        self._print_winner(game_state)
        self._game_num += 1
        if game_state == GameState.DRAW:
            self._draws += 1
        if self._game_num == self._max_games:
            self._running = False
            return
        self._notify_end(game_state)
        self._restart()

    def switch_players(self):
        self._player_on_roll = Stone.O_PLAYER if self._player_on_roll == Stone.X_PLAYER else Stone.X_PLAYER

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
        if game_state != GameState.PLAYING:
            self._game_over(game_state)

        else:
            self._roll_ended = True

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
            if self._game_num == self._max_games:
                break

            if self._roll_ended:
                self._player_on_roll = Stone.O_PLAYER if self._player_on_roll == Stone.X_PLAYER else Stone.X_PLAYER
                self._roll_ended = False
                self.next_roll()


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
                self._window[f'{row}-{col}'].update(disabled=(stone != Stone.EMPTY), **self._get_symbol(stone))

    def play(self, x, y):
        super().play(x, y)
        self._update_symbols()

    def on_event(self, *args, **kwargs):
        self.get_player_on_roll().on_event(*args, **kwargs)

    def _work(self):
        first = True

        while self._running is True:
            if self._game_num == self._max_games:
                self._running = False
                break
            event, values = self._window.read(timeout=100)
            if event == WIN_CLOSED:
                self._running = False
                return

            if first:
                first = False
                self._update_symbols()

            self.on_event(event, values)
            if self._roll_ended:
                self._player_on_roll = Stone.O_PLAYER if self._player_on_roll == Stone.X_PLAYER else Stone.X_PLAYER
                self._roll_ended = False
                self.next_roll()

    def start(self):
        if self._running is True:
            raise RuntimeError('Cannot run one window twice')

        self._running = True
        self._work()
