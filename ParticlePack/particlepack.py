import pygame
from math import sin, cos, radians
from random import randint

def randomColor(R = None, G = None, B = None, Rmax = 255, Rmin = 0, Bmax = 255, Bmin = 0, Gmax = 255, Gmin = 0,):
    if R == None:
        R = randint(Rmin,Rmax)
    if G == None:
        G = randint(Gmin,Gmax)
    if B == None:
        B = randint(Bmin,Bmax)
    return (R, G, B)

def randomBlue():
    return randomColor(B = 255, Rmax = 70, Gmax = 150)

def updatedraw(objects, delta, screen):
    for i, obj in enumerate(objects):
        if obj == None:
            while i < len(objects)-1 and objects[len(objects)-1] == None:
                objects.pop()
            objects[i], objects[len(objects)-1] = objects[len(objects)-1], objects[i]
            if objects[i]:
                objects[i].update(delta)
                objects[i].draw(screen)
            objects.pop()
        elif obj.dead == True:
            objects[i] = None
        else:
            obj.update(delta)
            obj.draw(screen)

class Particle():
    """Defines a single particle with an (x,y) angle, velocity, color, life, size, and gravity"""
    def __init__(self, xy, a, v, c=None, l=2, s=4, ppm=512, g=10):
        self.x, self.y = xy
        self.a = a
        self.v = v
        if c == None:
            self.c = randomColor()
        else:
            self.c = c
        self.l = l
        self.s = s
        self.g = g*ppm
        self.t = 0
        self.dead = False

    def __repr__(self):
        return 'Particle'

    def update(self, delta):
        if self.t >= self.l:
            self.dead = True
        delta /= 1000
        self.t += delta
        self.x += cos(radians(self.a))*self.v*delta
        self.y += sin(radians(self.a))*self.v*delta
        self.y += delta*self.t*self.g

    def draw(self, screen):
        pygame.draw.circle(screen, self.c, (round(self.x), round(self.y)), self.s)

class Rain():
    def __init__(self, xy, wh, h=0.5, a=0):
        self.x, self.y = xy
        self.w, self.h = wh
        self.h = h
        self.a = a
        self.raining = False
    class spout():
        def __init__(self, xy, drips=5, vel=10, a,)
    def update(self, delta):
        delta /= 1000
        if raining:
            

    def begin(self):
        self.raining = True
    def stop(self):
        self.raining = False