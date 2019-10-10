import time


class Controller():

    def __init__(self, game_duration=45, game_resuming=15):
        self.game_duration = game_duration
        self.game_resuming = game_resuming
        self.started_at = None
        self.time_ref = time.time()
        self.time_counter = 0

    def start(self):
        if self.started_at == None:
            self.started_at = time.time()

    def end(self):
        self.started_at = None

    def get_time(self):
        if self.started_at != None:
            return int(time.time() - self.started_at)
        return 0

    def every_seconds(self, seconds):
        if time.time() - self.time_ref > seconds:
            self.time_ref = time.time()
            self.time_counter = 0
            return True
        else:
            self.time_counter += time.time() - self.time_ref
            return False

    def is_playing(self):
        return self.started_at != None and self.get_time() > 0 and self.get_time() < self.game_duration

    def is_resuming(self):
        return self.started_at != None and self.get_time() >= self.game_duration and self.get_time() <= (self.game_duration + self.game_resuming)

    def is_standing_by(self):
        return self.started_at == None

    def is_finished(self):
        return self.get_time() > (self.game_duration + self.game_resuming)

    def get_state(self):
        if self.is_playing(): return '{} secs'.format(self.game_duration - self.get_time())
        if self.is_resuming(): return 'Credits'
        if self.is_standing_by(): return 'Waiting'
        if self.is_finished(): return 'Finished'
