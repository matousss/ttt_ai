from PySimpleGUI import theme

from ai.data import data_from_logs, save_data
from ai.trainer import Trainer
from minimax.player import MiniMaxPlayer
from randomized.player import RandomPlayer


if __name__ == '__main__':
    theme('black')
    t = Trainer(RandomPlayer(0), MiniMaxPlayer(1), max_games=5000)
    t.start()

    data = data_from_logs(t.get_logs())
    save_data(*data, 'data_random-minimax.txt')

