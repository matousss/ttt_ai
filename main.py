from PySimpleGUI import theme

from minimax.player import MiniMaxPlayer
from tictactoe.players import HumanPlayer
from tictactoe.game_gui import TicTacToeGUI

if __name__ == '__main__':
    theme('black')
    t = TicTacToeGUI(HumanPlayer, MiniMaxPlayer, max_games=20)
    t.start()

    print(t.get_scores())
