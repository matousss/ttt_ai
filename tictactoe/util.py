import base64
import random
from copy import deepcopy
from os import path


class Stone:
    EMPTY = 0
    X_PLAYER = -1
    O_PLAYER = 1


class GameState:
    PLAYING = Stone.EMPTY
    X_WON = Stone.X_PLAYER
    O_WON = Stone.O_PLAYER
    DRAW = 3


STONE_STR = {
    Stone.EMPTY: ' ',
    Stone.X_PLAYER: '⨉',
    Stone.O_PLAYER: '○',
}

ROOT_DIR = path.abspath(
    # parent dir
    path.join(
        # current dir
        path.dirname(path.abspath(__file__)),
        path.pardir
    )
)

STONES_ASSETS = {
    Stone.X_PLAYER: path.join(ROOT_DIR, 'assets/x.png'),
    Stone.O_PLAYER: path.join(ROOT_DIR, 'assets/o.png'),
}

DEFAULT_DESK = [
    [Stone.EMPTY, Stone.EMPTY, Stone.EMPTY],
    [Stone.EMPTY, Stone.EMPTY, Stone.EMPTY],
    [Stone.EMPTY, Stone.EMPTY, Stone.EMPTY],
]


def get_default_desk():
    return deepcopy(DEFAULT_DESK)


def convert_img_base64(src):
    with open(src, "rb") as img_file:
        return base64.b64encode(img_file.read())


STONES_BASE64 = {}


def init_assets():
    global STONES_BASE64
    for s in STONES_ASSETS.keys():
        STONES_BASE64[s] = convert_img_base64(STONES_ASSETS[s])


init_assets()


def _default_chooser(game: 'TicTacToe'):
    return Stone.X_PLAYER if bool(random.randint(0, 1)) else Stone.O_PLAYER


def check_win(desk):
    # check cols
    for i in range(3):
        a = desk[i][0]
        if a == Stone.EMPTY:
            continue
        for j in range(1, 3):
            if desk[i][j] != a:
                break
        else:
            return a

    # check cols
    for i in range(3):
        a = desk[0][i]
        if a == Stone.EMPTY:
            continue
        for j in range(1, 3):
            if desk[j][i] != a:
                break
        else:
            return a

    # check diagonals
    for i in range(2):
        a = desk[i * 2][0]
        if a == Stone.EMPTY:
            continue
        for j in range(1, 3):

            if desk[abs(i * 2 - j)][j] != a:
                break

        else:
            return a

    # check draw
    for col in desk:
        for stone in col:
            if stone == Stone.EMPTY:
                return GameState.PLAYING

    return GameState.DRAW


def get_possible_moves(board):
    moves = []

    for x in range(3):
        for y in range(3):
            if board[x][y] == Stone.EMPTY:
                moves.append((x, y))

    return moves
