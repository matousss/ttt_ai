from ai.data import DeskLog, Stroke
from tictactoe.game import TicTacToe
from tictactoe.game_gui import TicTacToeGUI


class Trainer(TicTacToe):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_stroke = None
        self._log = DeskLog()
        self._logs = []

    def _print_winner(self, game_state):
        print(self._game_num)

    def _game_over(self, game_state):
        self._log.add_stroke(self._last_stroke)
        self._log.set_winner(game_state)
        self._logs.append(self._log)

        self._log = DeskLog()
        self._last_stroke = None

        super()._game_over(game_state)

    def play(self, x, y):
        self._last_stroke = Stroke(x, y, self.get_player_on_roll().color)
        super().play(x, y)

        if self._last_stroke:
            self._log.add_stroke(self._last_stroke)

    def get_logs(self):
        return self._logs


class TrainerGUI(Trainer, TicTacToeGUI):
    def __init__(self, *args, **kwargs):
        super(TrainerGUI, self).__init__(*args, **kwargs)

    def _print_winner(self, game_state):
        TicTacToe._print_winner(self, game_state)
