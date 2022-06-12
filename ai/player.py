import numpy as numpy

from tictactoe.players import Player


class AIPlayer(Player):
    def __init__(self, color, model):
        super().__init__(color)
        self.model = model

    def on_roll(self, *args, **kwargs):
        p = self.model.predict(numpy.array(self.game.get_desk()).flatten())
        print(p)
        # todo handle result
