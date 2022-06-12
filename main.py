from time import sleep

from PySimpleGUI import theme

from ai.data import data_from_logs, save_data
from ai.trainer import TrainerGUI
from tictactoe.players import HumanPlayer
from tictactoe.game import TicTacToeGUI

if __name__ == '__main__':
    theme('black')
    t = TrainerGUI(HumanPlayer(0), HumanPlayer(1), choose_next_player=lambda game: 1)
    t.start()
    while t.is_running():
        sleep(.1)

    data = data_from_logs(t.get_logs())

    save_data(*data, 'data.txt')
