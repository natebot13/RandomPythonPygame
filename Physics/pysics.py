import pygame
import math
import random

class physicsObject():
	def __init__(self, obj, center = (0,0)):
		self.center = center
		self.xVelocity = 0
		self.yVelocity = 0

if __name__ == "__main__":
	pygame.init()
	FPS = 30
	SIZE = (512,512)
	clock = pygame.time.Clock()
	SCREEN = pygame.display.set_mode(SIZE)
	pygame.display.set_caption('Physics')
	createBlocks()
	while True:
