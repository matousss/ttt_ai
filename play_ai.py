import numpy
from PySimpleGUI import theme
from keras.saving.save import load_model

from ai.player import AIPlayer
from tictactoe.game import TicTacToeGUI
from tictactoe.players import HumanPlayer

if __name__ == '__main__':
    theme('black')
    model = load_model('model.h5')
    # TicTacToeGUI(HumanPlayer(0), AIPlayer(1, model)).start()
    d = numpy.array([
        [-1, -1, 0],
        [-1, -1, -1],
        [-1, -1, -1],
                                   ]).reshape(-1, 9)

    print(d)

    p = model.predict(d)

    print(p)
