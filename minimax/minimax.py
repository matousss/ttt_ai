import math
from copy import deepcopy

from tictactoe.util import Stone, check_win, GameState, get_possible_moves


def imaginary_move(x, y, board, color):
    new = deepcopy(board)
    new[x][y] = color

    return new


def get_color(maximizer_turn: bool, maximizer_id: int):
    if maximizer_turn:
        return Stone.O_PLAYER if maximizer_id == Stone.X_PLAYER else Stone.X_PLAYER
    return maximizer_id


def best_move(desk, color):
    best_score = -math.inf
    best = None
    board = desk
    moves = get_possible_moves(board)

    # dont't calculate first move, because it is always top-left corner
    if len(moves) == 9:
        return 0, 0

    for move in moves:
        score = minimax(False, color, imaginary_move(*move, board, color))
        if score > best_score:
            best_score = score
            best = move

    return best


def minimax(maximizer_turn: bool, maximizer_id: int, board):
    game_state = check_win(board)
    if game_state == GameState.DRAW:
        return 0
    elif game_state != GameState.PLAYING:
        return (1 if game_state == maximizer_id else -1) * 1000 * (1 + len(get_possible_moves(board)))
    # scores = []
    # for move in get_possible_moves(board):
    #     scores.append(minimax(not maximizer_turn,
    #                           maximizer_id,
    #                           imaginary_move(*move, board, get_color(maximizer_turn, maximizer_id))))
    #
    # return max(scores) if maximizer_turn else min(scores)
    moves = get_possible_moves(board)

    if maximizer_turn:
        best_score = -math.inf
        for move in moves:
            score = minimax(False, maximizer_id, imaginary_move(*move, board, get_color(maximizer_turn, maximizer_id)))
            if score > best_score:
                best_score = score
            score = minimax(False, maximizer_id, imaginary_move(*move, board, get_color(maximizer_turn, maximizer_id)))
            if score > best_score:
                best_score = score

    else:
        best_score = math.inf
        for move in moves:
            score = minimax(True, maximizer_id, imaginary_move(*move, board, get_color(maximizer_turn, maximizer_id)))
            if score < best_score:
                best_score = score

    return best_score
