from PySimpleGUI import theme

from ai.data import data_from_logs, save_data
from ai.trainer import TrainerGUI
from minimax.player import MiniMaxPlayer
from tictactoe.players import HumanPlayer
from tictactoe.util import Stone

if __name__ == '__main__':
    theme('black')
    t = TrainerGUI(HumanPlayer(Stone.X_PLAYER), MiniMaxPlayer(Stone.O_PLAYER), max_games=20)
    t.start()

    data = data_from_logs(t.get_logs())
    save_data(*data, 'data_player-minimax.txt')
