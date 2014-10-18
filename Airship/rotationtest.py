import pygame

pygame.init()

SCREEN = pygame.display.set_mode((512,512))

clock = pygame.time.Clock()

wheel = pygame.image.load("wheel.png")
FPS = 60

deg = 0

while True:
	for event in pygame.event.get():
		pass
	SCREEN.fill((255,255,255))
	drawthis = pygame.transform.rotate(wheel, deg)
	SCREEN.blit(drawthis, (256-drawthis.get_rect().right/2, 256-drawthis.get_rect().bottom/2))
	pygame.display.update()
	deg+=1
	clock.tick(FPS)
