import pygame
import os

class Component:
    def CID(self):
        return self.__class__.__name__

class Position(Component):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    @property
    def xy(self):
        return (self.x, self.y)

class Velocity(Component):
    def __init__(self, speed=50):
        self.spdCONST = speed
        self.speed = 0
        self.angle = 0

class Collidable(Component):
    def __init__(self, collisionrect, scalefactor, prescale = True):
        if prescale:
            collisionrect.x *= scalefactor
            collisionrect.y *= scalefactor
            collisionrect.width *= scalefactor
            collisionrect.height *= scalefactor
        self.xoffset = collisionrect.x
        self.yoffset = collisionrect.y
        self.collisionrect = collisionrect
        self.colliding = {'right': False, 'up': False, 'left': False, 'down': False}

    @property
    def xyoffset(self):
        return (self.xoffset, self.yoffset)

class Collider(Component):
    def __init__(self, collisionrect):
        self.collisionrect = collisionrect

class Renderable(Component):
    def __init__(self, scalefactor, filename = None, surface = None):
        self.scalefactor = scalefactor
        if filename:
            self.sprite = pygame.image.load(os.path.join('textures', filename))
        elif surface:
            self.sprite = surface
        else:
            self.sprite = None

class Animated(Component):
    def __init__(self, spritewidth = 16, animation_pattern = (0, 1, 0, 2), animation_rate = 7):
        self.active = False
        self.t = 0.0
        self.spritewidth = spritewidth
        self.pattern = animation_pattern
        self.rate = (1 / animation_rate) * 1000
        self.ptrnPos = 0

    def getFrame(self, dt):
        if self.active:
            self.t += dt
            if self.t > self.rate:
                self.t = 0
                self.ptrnPos += 1
                if self.ptrnPos == len(self.pattern):
                    self.ptrnPos = 0
        else:
            self.ptrnPos = 0
        return self.pattern[self.ptrnPos]

class Multifaced(Component):
    def __init__(self, spriteheight = 16):
        self.spriteheight = spriteheight
        self.face = 0

class MovementAnimation(Component):
    def __init__(self):
        pass

class Controllable(Component):
    def __init__(self, controls):
        self.controls = controls
        self.events = []

    def getKeyDownEvents(self, eventTypes):
        self.events, events = self.keeplose(pygame.KEYDOWN, eventTypes)
        return events

    def getKeyUpEvents(self, eventTypes):
        self.events, events = self.keeplose(pygame.KEYUP, eventTypes)
        return events

    def keeplose(self, eventtype, wantedevents):
        keep = []
        lose = []
        for each in self.events:
            if each.type == eventtype and each.key in wantedevents:
                lose.append(each)
            else:
                keep.append(each)
        return keep, lose

class Movable(Component):
    def __init__(self, controls):
        self.controls = controls

class Unique(Component):
    def __init__(self):
        pass