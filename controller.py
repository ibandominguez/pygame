import time


class Controller():

    GAME_DURATION = 45
    GAME_RESUMING = 15

    def __init__(self):
        self.started_at = None

    def start(self):
        if self.started_at == None:
            self.started_at = time.time()

    def end(self):
        self.started_at = None

    def get_time(self):
        if self.started_at != None:
            return int(time.time() - self.started_at)
        return None

    def is_playing(self):
        return self.started_at != None and self.get_time() > 0 and self.get_time() < self.GAME_DURATION

    def is_resuming(self):
        return self.started_at != None and self.get_time() >= self.GAME_DURATION and self.get_time() <= self.GAME_RESUMING

    def is_standing_by(self):
        return self.started_at == None

    def is_finished(self):
        return self.get_time() > (self.GAME_DURATION + self.GAME_RESUMING)
