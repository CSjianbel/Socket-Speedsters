class GameInfo:

    def __init__(self):
        self.started = False

    def game_status(self):
        return self.started

    def game_finished(self):
        self.started = False

    def start_game(self):
        self.started = True
