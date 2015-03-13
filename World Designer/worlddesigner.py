import sge, random

class Game(sge.Game):

    def event_game_start(self):
        pass

    def event_step(self, time_passed, delta_mult):
        pass

    def event_key_press(self, key, char):
        pass

    def event_close(self):
        pass

    def event_paused_key_press(self, key, char):
        pass

    def event_paused_close(self):
        pass

class terrainBlock(sge.Object):

    def __init__(self):
        super().__init__(x, y, sprite=sprite)