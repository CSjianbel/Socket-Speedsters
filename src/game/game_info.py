import time

class GameInfo:

    def __init__(self):
        self.started = False

    def game_finished(self):
        self.started = False

    def start_level(self):
        self.started = True


