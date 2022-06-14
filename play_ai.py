import numpy
from PySimpleGUI import theme
from keras.saving.save import load_model

from ai.player import AIPlayer
from minimax.minimax import best_move
from tictactoe.game import TicTacToeGUI
from tictactoe.players import HumanPlayer

if __name__ == '__main__':
    theme('black')
    model = load_model('model.h5')
    # TicTacToeGUI(HumanPlayer, AIPlayerBuilder(model)).start()
    n =[
        [0, -1, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    d = numpy.array(n).reshape(-1, 9)

    print(d)
    print(best_move(n, 1))
    p = model.predict(d)

    print(p)
    print(p[0][0])
    print(max(p[0]))