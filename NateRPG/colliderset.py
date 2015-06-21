import pygame
import sys
import os

if __name__ == "__main__":

    TILESIZE = (16, 16)
    SCALEFACTOR = 30
    WIDTH = TILESIZE[0] * SCALEFACTOR
    HEIGHT = TILESIZE[1] * SCALEFACTOR
    SIZE = (WIDTH,HEIGHT)
    FPS = 30
    CLOCK = pygame.time.Clock()

    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Set Colliders')

    texture = pygame.image.load(os.path.join("textures", sys.argv[1])).convert_alpha()
    tile = pygame.Surface(TILESIZE)
    colSurf = pygame.Surface(TILESIZE)
    w, h = TILESIZE
    r = texture.get_rect()
    xTiles = r.width // w
    yTiles = r.height // h
    tilenum = 0

    changed = True
    save = False
    export = False
    topleft = None
    bottomright = None

    colliders = {}

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RIGHT:
                    if tilenum < xTiles * yTiles:
                        tilenum += 1
                        changed = True
                if event.key == pygame.K_LEFT:
                    if tilenum > 0:
                        tilenum -= 1
                        changed = True
                if event.key == pygame.K_j:
                    num = input("Jump to: ")
                    tilenum = int(num)
                    changed = True
                if event.key == pygame.K_RETURN:
                    save = True
                if event.key == pygame.K_s:
                    export = True


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if tilenum > 0:
                        tilenum -= 1
                        changed = True
                if event.button == 5:
                    if tilenum < (xTiles * yTiles) - 1:
                        tilenum += 1
                        changed = True
                if event.button == 1:
                    topleft = (event.pos[0]//SCALEFACTOR,event.pos[1]//SCALEFACTOR)
                    print(topleft)
                if event.button == 3:
                    bottomright = (event.pos[0]//SCALEFACTOR,event.pos[1]//SCALEFACTOR)
                    print(bottomright)

        if changed:
            topleft = None
            bottomright = None
            changed = False
        x = (tilenum % xTiles) * TILESIZE[0]
        y = (tilenum // xTiles) * TILESIZE[1]
        tile.fill((255,255,255))
        tile.blit(texture, (0, 0), pygame.Rect((x, y),TILESIZE))

        if topleft and bottomright:
            size = ((bottomright[0] + 1) - topleft[0], (bottomright[1] + 1) - topleft[1])
            pygame.draw.rect(tile, (255, 0, 0), pygame.Rect(topleft, size), 1)
            if save:
                colliders[tilenum] = topleft + size
                print("Recorded tile:", tilenum, topleft, bottomright)
                save = False
        if export and colliders:
            filename = sys.argv[1][:sys.argv[1].find('.')]
            with open(os.path.join('colliders', filename + '.col'), 'w') as f:
                for num in colliders:
                    f.write(str(num) + ':' + ','.join([str(s) for s in colliders[num]]) + '\n')
            print("Exported all tiles!")
            export = False

        SCREEN.fill((255, 255, 255))
        pygame.transform.scale(tile, SCREEN.get_rect().size, SCREEN)
        pygame.display.update()
        CLOCK.tick()