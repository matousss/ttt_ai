def raise_(ex):
    raise ex


class Player:
    def __init__(self, color):
        self.color = color
        self.desk = None

    def set_desk(self, desk):
        self.desk = desk

    def play(self, x, y):
        self.desk.play(x, y)

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
        self.play(x, y)
