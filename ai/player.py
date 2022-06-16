import math

import numpy as numpy

from ai.data import get_data_desk
from tictactoe.players import Player
from tictactoe.util import Stone


class AIPlayerBuilder:
    def __init__(self, model):
        self.model = model

    def __call__(self, *args, **kwargs):
        return AIPlayer(*args, model=self.model, **kwargs)


class AIPlayer(Player):
    def __init__(self, *args, model, **kwargs):
        super().__init__(*args, **kwargs)
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

        d = numpy.array(transformed).reshape(-1, 9)
        best_move = 0, 0
        best = -1

        predict = self.model.predict(d).reshape(3, 3)
        print(predict.reshape(3, 3))
        for x in range(3):
            for y in range(3):
                if predict[x][y] > best and desk_state[x][y] == Stone.EMPTY:
                    best_move = x, y
                    best = predict[x][y]

        print(best_move)
        self.play(*best_move)
