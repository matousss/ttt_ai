from PySimpleGUI import theme

from minimax.player import MiniMaxPlayer
from tictactoe.players import HumanPlayer
from tictactoe.game import TicTacToeGUI

if __name__ == '__main__':
    theme('black')
    t = TicTacToeGUI(HumanPlayer(0), MiniMaxPlayer(1), max_games=20)
    t.start()

    print(t.get_scores())
