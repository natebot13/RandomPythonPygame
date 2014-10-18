import pygame, sys, math, random
pygame.init()

SIZE = (400,300)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Terrain Tests')

FPS = 30
fpsClock = pygame.time.Clock()

BROWN = (100,50,0)

blocks = [pygame.Rect((0,0),SIZE)]

while True:
	for block in blocks:
		pygame.draw.rect(SCREEN, BROWN, block)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			mousepos = event.pos
				
				
	pygame.display.update()
	
