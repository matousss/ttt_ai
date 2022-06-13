import numpy as numpy

from ai.data import get_data_desk
from tictactoe.players import Player
from tictactoe.util import Stone


class AIPlayer(Player):
    def __init__(self, color, model):
        super().__init__(color)
        self.model = model
        self._transformer = {
            self.color: 1,
            Stone.EMPTY: 0,
            Stone.O_PLAYER if self.color == Stone.X_PLAYER else Stone.X_PLAYER: -1
        }

    def on_roll(self, *args, **kwargs):
        desk_state = self.game.get_desk()
        transformed = get_data_desk()
        for x in range(3):
            for y in range(3):
                transformed[x][y] = self._transformer[desk_state[x][y]]

        p = self.model.predict(numpy.array(transformed).flatten())
        print(p)
        # todo handle result
