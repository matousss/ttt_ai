def raise_(ex):
    raise ex


class Player:
    def __init__(self, color):
        self.color = color
        self.game = None
        self.score = 0

    def set_game(self, game):
        self.game = game

    def play(self, x, y):
        self.game.play(x, y)

    def on_roll(self, *args, **kwargs):
        pass

    def on_event(self, *args, **kwargs):
        pass

    def game_over(self, winner):
        pass


class HumanPlayer(Player):
    def on_roll(self, *args, **kwargs):
        super().on_roll(*args, **kwargs)

    def on_event(self, event, *args, **kwargs):
        y, x = (int(a) for a in event.split('-'))
        if self.game.get_desk()[x][y] == Stone.EMPTY:
            self.play(x, y)
