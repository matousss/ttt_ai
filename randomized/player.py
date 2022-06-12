from random import choice

from tictactoe.players import Player
from tictactoe.util import get_possible_moves


class RandomPlayer(Player):
    def on_roll(self, *args, **kwargs):
        desk = self.game.get_desk()
        moves = get_possible_moves(desk)
        self.play(*choice(moves))
