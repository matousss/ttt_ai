from copy import deepcopy

from tictactoe.util import get_default_desk


class Stroke:
    def __init__(self, x, y, stone):
        self.x = x
        self.y = y
        self.stone = stone


class DeskLog:
    def __init__(self):
        self._strokes = []
        self._winner = -1

    def add_stroke(self, stroke):
        self._strokes.append(stroke)

    def get_strokes(self):
        val = []
        desk_state = get_default_desk()
        for stroke in self._strokes:
            val.append((deepcopy(desk_state), stroke))
            desk_state[stroke.x][stroke.y] = stroke.stone

    @staticmethod
    def locked(self):
        raise Exception("Log ended")

    def set_winner(self, winner):
        self._winner = winner


def lock_log(log: DeskLog, winner):
    log.set_winner(winner)
    log.get_strokes = type(DeskLog.get_strokes)(DeskLog.locked, log, DeskLog)
    log.add_stroke = type(DeskLog.add_stroke)(DeskLog.locked, log, DeskLog)
