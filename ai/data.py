from copy import deepcopy

from tictactoe.util import get_default_desk, STONE_STR, GameState


class Stroke:
    def __init__(self, x, y, stone):
        self.x = x
        self.y = y
        self.stone = stone

    def __str__(self):
        return f'{self.x}-{self.y}: {STONE_STR[self.stone]}'


class DeskLog:
    def __init__(self):
        self._strokes = []
        self._winner = None

    def add_stroke(self, stroke):
        if self._winner is not None:
            self._locked()
        self._strokes.append(stroke)

    def get_strokes(self):
        val = []
        desk_state = get_default_desk()
        for stroke in self._strokes:
            val.append((deepcopy(desk_state), stroke))
            desk_state[stroke.x][stroke.y] = stroke.stone
        return val

    @staticmethod
    def _locked():
        raise Exception("Log ended")

    def set_winner(self, winner):
        if self._winner is not None:
            self._locked()
        self._winner = winner

    def __str__(self):
        s = self.get_strokes()
        string = ''

        for i in range(len(s)):
            desk = s[i][0]
            desk[s[i][1].x][s[i][1].y] = s[i][1].stone
            string += f'{i+1}.\n┌──────┐\n'
            for x in range(3):
                for y in range(3):
                    string += f' {STONE_STR[desk[x][y]]}'
                string += '\n'
            string += '└──────┘\n'
        if self._winner:
            string += f'Winner: {"Draw" if self._winner == GameState.DRAW else STONE_STR[self._winner]}'
        return string
