import base64
import random
from copy import deepcopy


class Stone:
    EMPTY = -1
    X_PLAYER = 0
    O_PLAYER = 1


class GameState:
    PLAYING = -1
    X_WON = Stone.X_PLAYER
    O_WON = Stone.O_PLAYER
    DRAW = 3


STONE_STR = {
    Stone.EMPTY: '',
    Stone.X_PLAYER: '⨉',
    Stone.O_PLAYER: '○',
}

STONES_ASSETS = {
    Stone.X_PLAYER: './assets/x.png',
    Stone.O_PLAYER: './assets/o.png',
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
    for i in range(3):
        a = desk[i][0]
        if a == -1:
            continue
        for j in range(1, 3):
            if desk[i][j] != a:
                break
        else:
            return a

    for i in range(3):
        a = desk[0][i]
        if a == -1:
            continue
        for j in range(1, 3):
            if desk[j][i] != a:
                break
        else:
            return a

    # check diagonals
    for i in range(2):
        a = desk[i * 2][0]
        if a == -1:
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
