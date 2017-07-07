import pygame
from particlepack import *
from random import randint

def main():
    FPS = 60
    SCREEN = pygame.display.set_mode((512,512))#, pygame.FULLSCREEN)
    SIZE = SCREEN.get_size()
    WIDTH, HEIGHT = SIZE
    pygame.display.set_caption("Particle Pack Tests")
    CLOCK = pygame.time.Clock()

    running = True

    objects = []

    while running:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                objects.append(Particle(event.pos, -45, 100, c=randomBlue(), g=5))

        SCREEN.fill((0,0,0))
        delta = CLOCK.get_time()
        updatedraw(objects, delta, SCREEN)
        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main()