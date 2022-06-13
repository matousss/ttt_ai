from tictactoe.util import Stone


def raise_(ex):
    raise ex


class Player:
    def __init__(self, color, game):
        self.color = color
        self.game = game
        self.score = 0

    def play(self, x, y):
        self.game.play(x, y)

    def on_roll(self, *args, **kwargs):
        pass

    def on_event(self, *args, **kwargs):
        pass

    def game_over(self, winner):
        if winner == self.color:
            self.increase_score()

    def increase_score(self):
        self.score += 1


class HumanPlayer(Player):
    def on_event(self, event, *args, **kwargs):
        if event == '__TIMEOUT__':
            return
        y, x = (int(a) for a in event.split('-'))
        if self.game.get_desk()[x][y] == Stone.EMPTY:
            self.play(x, y)
