from time import sleep

from PySimpleGUI import theme

from tictactoe.players import HumanPlayer
from tictactoe.game import TicTacToeGUI

if __name__ == '__main__':
    theme('black')
    t = TicTacToeGUI(HumanPlayer(0), HumanPlayer(1), choose_next_player=lambda game: 1)
    t.start()
    while t.is_running():
        sleep(.1)
