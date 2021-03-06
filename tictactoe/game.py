from copy import deepcopy

from tictactoe.players import Player
from tictactoe.util import STONE_STR, Stone, GameState, get_default_desk, _default_chooser, check_win


# Class represents a game of TicTacToe
class TicTacToe:
    def __init__(self, player_class1, player_class2, *, choose_next_player=_default_chooser, max_games=None):
        self._stones = get_default_desk()
        player1 = player_class1(Stone.X_PLAYER, self)
        player2 = player_class2(Stone.O_PLAYER, self)
        self.players = (player1, player2)
        self._color_to_player = {
            player1.color: player1,
            player2.color: player2,
        }
        self._roll_ended = True
        self._max_games = max_games
        self._game_num = 0
        self._draws = 0

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

        self._notify_end(game_state)
        if self._game_num == self._max_games:
            self._running = False
            return
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

    def get_scores(self):
        return {
            'total': self._game_num,
            'draws': self._draws,
            STONE_STR[self.players[0].color]: self.players[0].score,
            STONE_STR[self.players[1].color]: self.players[1].score,
        }

    def start(self):
        while True:
            if self._game_num == self._max_games:
                break

            if self._roll_ended:
                self._player_on_roll = Stone.O_PLAYER if self._player_on_roll == Stone.X_PLAYER else Stone.X_PLAYER
                self._roll_ended = False
                self.next_roll()
