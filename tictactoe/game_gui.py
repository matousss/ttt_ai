from PySimpleGUI import theme, Button, Window, WIN_CLOSED

from tictactoe.game import TicTacToe
from tictactoe.util import Stone, STONES_BASE64


# Game representation with GUI
class TicTacToeGUI(TicTacToe):
    BTN_SIZE = 120, 120

    @staticmethod
    def init_layout():
        layout = [[
            Button(key=f'{i}-{j}', image_data='', border_width=0, disabled_button_color=('black', 'black'))
            for i in range(3)
        ] for j in range(3)]
        return layout

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._running = False
        self._window = Window('TicTacToe', self.init_layout())

    """
    Check if game window is running
    """

    def is_running(self):
        return self._running

    @staticmethod
    def _get_symbol(_id: int):
        val = {
            'image_data': '',
            'image_size': TicTacToeGUI.BTN_SIZE,
        }
        if _id == Stone.EMPTY:
            return val

        val['image_data'] = STONES_BASE64[_id]

        return val

    def _update_symbols(self):
        for col in range(3):
            for row in range(3):
                stone = self._stones[col][row]
                self._window[f'{row}-{col}'].update(disabled=(stone != Stone.EMPTY), **self._get_symbol(stone))

    def play(self, x, y):
        super().play(x, y)
        self._update_symbols()

    def on_event(self, *args, **kwargs):
        self.get_player_on_roll().on_event(*args, **kwargs)

    def _work(self):
        first = True

        while self._running is True:
            if self._game_num == self._max_games:
                self._running = False
                break
            event, values = self._window.read(timeout=100)
            if event == WIN_CLOSED:
                self._running = False
                return

            if first:
                first = False
                self._update_symbols()

            self.on_event(event, values)
            if self._roll_ended:
                self._player_on_roll = Stone.O_PLAYER if self._player_on_roll == Stone.X_PLAYER else Stone.X_PLAYER
                self._roll_ended = False
                self.next_roll()

    def start(self):
        if self._running is True:
            raise RuntimeError('Cannot run one window twice')

        self._running = True
        theme('black')
        self._work()
