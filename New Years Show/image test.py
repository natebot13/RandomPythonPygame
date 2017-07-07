import pygame

SCREEN = pygame.display.set_mode((640,640))

image = pygame.image.load("A_little_late_but__Santa_s_Sleigh.jpg").convert()

SCREEN.blit(image, (0,0))
pygame.display.update()

pygame.time.wait(1000)
