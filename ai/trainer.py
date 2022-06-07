from tictactoe.game import TicTacToe


class Trainer(TicTacToe):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _game_over(self, game_state):
        super()._game_over(game_state)


