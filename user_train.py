from PySimpleGUI import theme

from ai.data import data_from_logs, save_data
from ai.trainer import TrainerGUI
from minimax.player import MiniMaxPlayer
from tictactoe.players import HumanPlayer

if __name__ == '__main__':
    theme('black')
    t = TrainerGUI(HumanPlayer(0), MiniMaxPlayer(1), max_games=20)
    t.start()

    data = data_from_logs(t.get_logs())
    save_data(*data, 'data_player-minimax.txt')
