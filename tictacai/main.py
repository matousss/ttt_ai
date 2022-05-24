from time import sleep

from PySimpleGUI import theme

# IMAGE_O = 'assets/o.png'
# IMAGE_X = 'assets/x.png'
from players import HumanPlayer
from tictacai.tictactoe import TicTacToeGUI

if __name__ == '__main__':
    theme('black')
    t = TicTacToeGUI(HumanPlayer(0), HumanPlayer(1))

    t.start()
    while t.is_running():
        sleep(.1)
        # t.set_stone(random.randrange(0, 3), random.randrange(0, 3), random.randrange(1, 3))
        # print(t.get_desk())
