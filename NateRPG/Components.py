import pygame
import os

class Component:
    def CID(self):
        return self.__class__.__name__

class Position(Component):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    @property
    def xy(self):
        return (self.x, self.y)

class Velocity(Component):
    def __init__(self, speed=5):
        self.spdCONST = speed
        self.speed = 0
        self.angle = 0

class Renderable(Component):
    def __init__(self, filename, spritesize = (16, 16), animation_pattern = (0, 1, 0, 2), animation_rate = 1):
        self.t = 0.0
        self.spritesize = spritesize
        self.pattern = animation_pattern
        self.rate = (1 / animation_rate) * 1000
        w, h = spritesize
        image = pygame.image.load(os.path.join('textures', filename))
        self.images = {}
        numdirections = 4
        for d in range(numdirections):
            self.images[d] = image.subsurface(pygame.Rect((0, h * d), (image.get_width(), h)))
        self.ptrnPos = 0
        self.frame = animation_pattern[self.ptrnPos]

    def getFrame(self, row, dt):
        self.t += dt
        if self.t > self.rate:
            self.t = 0
            self.ptrnPos += 1
            if self.ptrnPos == len(self.pattern):
                self.ptrnPos = 0
            self.frame = self.pattern[self.ptrnPos]
        w = self.spritesize[0]
        return self.images[row].subsurface(pygame.Rect((w * self.frame, 0),(self.spritesize)))

class Controllable(Component):
    def __init__(self, controls):
        self.controls = controls
        self.events = []

class Unique(Component):
    def __init__(self):
        pass