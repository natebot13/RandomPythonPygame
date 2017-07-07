#!/usr/bin/python
import pygame, sys, math, random
import pyramid

class Sub():
	def __init__(self, (x,y)):
		width = 128
		height = 64
		self.center = (x,y)
		self.x = x-(width/2)
		self.y = y-(height/2)
		self.box = pygame.Surface((width, height))

	def draw(self, screen):
		self.box.fill((255,255,255))
		screen.blit(self.box, (self.x, self.y))

class VerticleWall():
	def __init__(self, center, flux, color=None):
		self.center = center
		self.flux = flux
		if not color:
			self.color = pyramid.randomColor()
		else:
			self.color = color


	def update():
		

def main():
	WIDTH = 512
	HEIGHT = 512
	SIZE = (WIDTH, HEIGHT)
	SCREEN = pygame.display.set_mode(SIZE)
	FPS = 60
	CLOCK = pygame.time.Clock()

	sub = Sub((256, 256))


	while True:
		SCREEN.fill((40,40,40))

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

		sub.draw(SCREEN)
		pygame.display.update()
		CLOCK.tick(FPS)


if __name__ == "__main__":
	main()