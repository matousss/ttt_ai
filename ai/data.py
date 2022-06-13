from copy import deepcopy

import numpy

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

    def get_winner(self):
        return self._winner

    def __str__(self):
        s = self.get_strokes()
        string = ''

        for i in range(len(s)):
            desk = s[i][0]
            desk[s[i][1].x][s[i][1].y] = s[i][1].stone
            string += f'{i + 1}.\n┌──────┐\n'
            for x in range(3):
                for y in range(3):
                    string += f' {STONE_STR[desk[x][y]]}'
                string += '\n'
            string += '└──────┘\n'
        if self._winner:
            string += f'Winner: {"Draw" if self._winner == GameState.DRAW else STONE_STR[self._winner]}'
        return string


def get_data_desk():
    return [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]


def get_right_strokes(log: DeskLog, include_draws):
    right_strokes = []
    for data in log.get_strokes():
        desk_state = data[0]
        stroke = data[1]

        if stroke.stone != log.get_winner() and (include_draws is False and log.get_winner() == GameState.DRAW):
            continue

        transformed_desk = get_data_desk()
        for x in range(3):
            for y in range(3):
                transformed_desk[x][y] = 1 if desk_state[x][y] == log.get_winner() else -1

        input_arr = numpy.array(desk_state).flatten()
        result = get_data_desk()
        result[stroke.x][stroke.y] = 1

        output_arr = numpy.array(result).flatten()

        right_strokes.append((input_arr, output_arr))

    return right_strokes


def data_from_logs(logs, include_draws=False):
    input_data = []
    output_data = []
    for log in logs:
        for data in get_right_strokes(log, include_draws):
            input_data.append(data[0])
            output_data.append(data[1])

    return numpy.array(input_data), numpy.array(output_data)


def save_data(input_data, output_data, filename):
    with open(filename, 'w+') as f:
        for i in range(len(input_data)):
            in_str = ','.join(str(x) for x in input_data[i])
            out_str = ','.join(str(x) for x in output_data[i])
            f.write(f'{in_str}:{out_str}\n')


def load_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        input_data = []
        output_data = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            in_str, out_str = line.split(':')
            input_data.append([int(x) for x in in_str.split(',')])
            output_data.append([int(x) for x in out_str.split(',')])

    return input_data, output_data
