import pygame
import numpy

def color_surface(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = red
    arr[:,:,1] = green
    arr[:,:,2] = blue

srf = pygame.display.set_mode((1024,1024))

image = pygame.image.load("circle.png")

color_surface(image, 0, 0, 255)

srf.blit(image, (0,0))
pygame.display.flip()
pygame.time.wait(3000)
