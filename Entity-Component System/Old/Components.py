class Component:
    def CID(self):
        return self.__class__.__name__

class Movable(Component):
    def __init__(self, x=0, y=0, xvel=0, yvel=0):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel

class Input(Component):
    def __init__(self):
        pass

class Unique(Component):
    def __init__(self):
        pass

