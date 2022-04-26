from PySimpleGUI import WIN_CLOSED

from tictactoe import TicTacToeGUI


class Player:
    def on_roll(self, color):
        pass


class HumanPlayer(Player, TicTacToeGUI):
    def on_roll(self, *args, **kwargs):
        super().on_roll(*args, **kwargs)

    def set_stone(self, x, y, stone):
        super().set_stone(x, y, stone)

    def on_event(self, event, values):
        x, y = (int(a) for a in event.split('-'))
        print(x, y)






