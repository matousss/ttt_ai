import os.path
from threading import Thread

import numpy
from PySimpleGUI import Window, Text, Quit, Button, WIN_CLOSED, Slider, Combo, Ok, Input, Save, Cancel, ProgressBar
from keras.saving.save import load_model

from ai.data import get_raw_data, data_from_logs, save_data
from ai.model import train, create_model
from ai.player import AIPlayer
from ai.trainer import Trainer
from minimax.player import MiniMaxPlayer
from randomized.player import RandomPlayer
from tictactoe.players import HumanPlayer


def use_current_ai(*args, **kwargs):
    return AIPlayer(load_model('./model.h5'), *args, **kwargs)


PLAYERS = {
    'Human': HumanPlayer,
    'Random': RandomPlayer,
    'MiniMax': MiniMaxPlayer,
    'AI': use_current_ai,
}

window = Window('TicTacToe - Model Creator', element_justification='center')
window.layout([
    [Text('Model Creator')],
    [Text('Player 1:'),
     Combo(['Random', 'MiniMax', 'AI'], key='player_1', readonly=True, default_value='Random')],
    [Text('Player 2:'),
     Combo(['Random', 'MiniMax', 'AI'], key='player_2', readonly=True, default_value='MiniMax')],
    [Text('Number of games:')],
    [Slider(
        range=(50, 5000), key='games_limit', default_value=250, text_color='white', orientation='horizontal',
        resolution=50
    )],
    [Button('Dump Data', button_color='red', key='dump'),
     Button('Generate Data', key='generate', button_color='green')],
    [Quit(button_color='red'), Button('Train Current Model', key='train_current'),
     Button('Train New Model', key='train_new')],
])


def prompt_for_train_props():
    prompt = Window(element_justification='center', title='Train Properties')
    prompt.layout([
        [Text('Epochs:')],
        [Slider(range=(50, 3000), default_value=300, key='epochs', text_color='white', orientation='horizontal',
                resolution=50, size=(40, 15))],
        [Text('Batch Size:')],
        [Slider(range=(1, 5096), default_value=32, key='batch_size', text_color='white', orientation='horizontal',
                size=(40, 15))],
        [Ok(button_color='green')],
        [Text('Note: This will take a while...')]
    ])
    e, values = prompt.read()
    if e != 'Ok':
        return 300, 32
    prompt.close()
    return int(values['epochs']), int(values['batch_size'])


def prompt_for_model_props():
    prompt = Window(element_justification='center', title='Model Properties')
    prompt.layout([
        [Text('Hidden Layers:')],
        [Text('', key='layers')],
        [Input(key='in'), Button('Add Layer', key='add')],
        [Button('Reset', key='reset', button_color='red'), Ok(button_color='green')]
    ])
    layers = []

    while True:
        e, values = prompt.read()
        if e == WIN_CLOSED:
            prompt.close()
            return None

        if e == 'Ok' and len(layers) > 0:
            prompt.close()
            return layers

        if e == 'add':
            try:
                layers.append(int(values['in']))
            except ValueError:
                pass

        if e == 'reset':
            layers = []
        prompt['layers'].update('\n'.join([f'Layer {i + 1}: {layers[i]}' for i in range(len(layers))]))


def show_stats(mae, mse):
    w = Window(element_justification='center', title='Model Stats')
    w.layout([
        [Text('MAE: {}'.format(mae))],
        [Text('MSE: {}'.format(mse))],
        [Cancel(button_color='red'), Save(button_color='green')]
    ])
    e, values = w.read()
    w.close()
    return e == 'Save'


def generate_data(players, games_limit):
    trainer = Trainer(*players, max_games=games_limit)
    trainer._print_winner = lambda winner: None
    w = Window(element_justification='center', title='Generating Data')
    w.layout([[ProgressBar(max_value=games_limit, key='progress', size=(40, 15))],
              [Text(f'Game 1/{games_limit}', key='text')]])

    t = Thread(target=trainer.start, daemon=True)
    w.read(timeout=0)
    t.start()

    while t.is_alive():
        e, _ = w.read(timeout=500)
        if e == WIN_CLOSED:
            if t.is_alive():
                t.join(timeout=0)
            w.close()
            return

        if e == 'start':
            w['start'].update(disabled=True)
            t.start()

        n = trainer._game_num + 1
        w['progress'].update(n)
        w['text'].update(f'Game {n}/{games_limit}')

    w.close()
    return data_from_logs(trainer.get_logs())


def main():
    while True:
        event, values = window.read()
        if event in (WIN_CLOSED, 'Quit'):
            return

        if event.startswith('train'):
            if not os.path.exists('./data.txt'):
                continue

            if event == 'train_current':
                model = load_model('./model.h5')
            elif event == 'train_new':
                hidden = prompt_for_model_props()
                model = create_model(hidden_layers=hidden)

            epochs, batch_size = prompt_for_train_props()

            raw = get_raw_data('./data.txt')
            data_x, data_y = numpy.array(raw[0]), numpy.array(raw[1])

            model, mae, mse = train(model, (data_x, data_y), epochs, batch_size, include_metrics=True)
            save = show_stats(mae, mse)

            if save:
                model.save('./model.h5')

        if event == 'dump':
            if os.path.exists('./data.txt'):
                os.remove("./data.txt")

        if event == 'generate':
            window.disappear()
            data = generate_data((PLAYERS[values['player_1']], PLAYERS[values['player_2']]), int(values['games_limit']))
            if not os.path.exists('./data.txt'):
                open('./data.txt', 'w+').close()
            save_data(*data, 'data.txt', append=True)
            window.reappear()


if __name__ == '__main__':
    main()
