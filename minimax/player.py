from minimax.minimax import best_move
from tictactoe.players import Player


class MiniMaxPlayer(Player):
    def on_roll(self, *args, **kwargs):
        move = best_move(self.game.get_desk(), self.color)
        self.play(*move)
