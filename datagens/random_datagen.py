from PySimpleGUI import theme

from ai.data import data_from_logs, save_data
from ai.trainer import Trainer
from minimax.player import MiniMaxPlayer
from randomized.player import RandomPlayer
from tictactoe.util import Stone

if __name__ == '__main__':
    theme('black')
    t = Trainer(RandomPlayer(Stone.X_PLAYER), MiniMaxPlayer(Stone.O_PLAYER), max_games=2)
    t.start()
    print(t.get_logs())
    data = data_from_logs(t.get_logs())
    print('data',data)
    save_data(*data, 'data_random-minimax.txt')
