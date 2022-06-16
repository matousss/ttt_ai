from PySimpleGUI import theme, Window, Text, WIN_CLOSED, Button, Quit, Slider, Radio, Ok
from keras.saving.save import load_model

from ai.player import AIPlayerBuilder
from minimax.player import MiniMaxPlayer
from tictactoe.game import TicTacToe
from tictactoe.players import HumanPlayer
from tictactoe.game_gui import TicTacToeGUI
from tictactoe.util import STONE_STR, Stone

GAMEMODE_KEYS = ['gamemode_01', 'gamemode_02', 'gamemode_03']
GAMEMODES = {
    GAMEMODE_KEYS[0]: (HumanPlayer, HumanPlayer),
    GAMEMODE_KEYS[1]: (HumanPlayer, MiniMaxPlayer),
    GAMEMODE_KEYS[2]: (HumanPlayer, AIPlayerBuilder(load_model('model.h5'))),
}
GAMEMODES_TEXT = {
    GAMEMODE_KEYS[0]: 'Human vs. Human',
    GAMEMODE_KEYS[1]: 'Human vs. MiniMax',
    GAMEMODE_KEYS[2]: 'Human vs. AI',
}
DEFAULT_GAMEMODE = GAMEMODE_KEYS[1]
SLIDER_MAX = 51

window = Window('TicTacToe - Main menu', element_justification='center')
window.layout([
    [Text('Gamemode:'), ],
    [
        Radio(GAMEMODES_TEXT[k], group_id='gamemode', key=k, default=(DEFAULT_GAMEMODE == k), enable_events=True) for k
        in GAMEMODE_KEYS
    ],
    [Text('User color:', key='color_text'), ],
    [
        Radio('X', group_id='color', key='color_x', default=True),
        Radio('O', group_id='color', key='color_o'),
    ],
    [Text('Number of games: '), Text('Infinite', key='games_limit_text')],
    [Slider(range=(1, SLIDER_MAX),
            default_value=SLIDER_MAX,
            size=(30, 15),
            orientation='horizontal',
            key='games_limit',
            disable_number_display=True, enable_events=True)],
    [Quit(button_color='red'),
     # Button('Retrain', key='retrain'),
     Button('Start', key='start', button_color='green')],
])


def retrain_popup():
    layout = [
        [Text('This action will overwrite current model.\nAre you sure?')],
        [Button('Yes', key='Yes'), Button('No', key='No')]
    ]
    win = Window(title='', layout=layout, element_justification='center', )
    try:
        return win.read()[0] == 'Yes'
    finally:
        win.close()


def show_score(scores):
    texts = [[Text(f'{k}: {scores[k]}')] for k in scores.keys()]

    score_window = Window('TicTacToe - Score', element_justification='right')
    score_window.layout([
        [Text('Score:   ')],
        *texts,
        [Ok()]],
    )
    score_window.read()
    score_window.close()

def main():
    while True:
        event, values = window.read()
        if event in (WIN_CLOSED, 'Quit'):
            return

        if event == 'games_limit':
            limit_text = str(int(values['games_limit']) if values['games_limit'] != SLIDER_MAX else 'Infinite')
            window['games_limit_text'].update(limit_text)
            continue

        # if event == 'retrain':
        #     window.disappear()
        #     do, data = retrain_popup()
        #     if do:
        #         print('Retraining')
        #     window.reappear()
        #     continue

        if event == 'start':
            window.disappear()
            for k in GAMEMODE_KEYS:
                if values[k]:
                    players = GAMEMODES[k]
                    break
            else:
                continue
            if values['color_o']:
                players = [players[1], players[0]]
                print(players)
            limit = int(values['games_limit']) if values['games_limit'] != 0 else None
            score = start_game(True, *players, limit)
            show_score(score)
            window.reappear()
            continue

        if event.startswith('gamemode'):
            visible = event != 'gamemode_01'
            window['color_x'].update(visible=visible)
            window['color_o'].update(visible=visible)
            window['color_text'].update(visible=visible)


def start_game(gui: bool, player_1, player_2, max_games: int):
    if gui:
        game = TicTacToeGUI(player_1, player_2, max_games=max_games)

    else:
        game = TicTacToe(player_1, player_2, max_games=max_games)

    game.start()
    return game.get_scores()


if __name__ == '__main__':
    theme('black')
    main()
