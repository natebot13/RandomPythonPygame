import os, sys, pygame

def loadColliders(self, collidersfile):
        colliders = {}
        with open(os.path.join('colliders', collidersfile)) as f:
            for line in f:
                numwh = line.split(':')
                wh = numwh[1].split(',')
                numwh = int(numwh[0])
                wh = [int(n) for n in wh]
                colliders[numwh] = {}
                for i in range(len(wh)//4):
                    colliders[numwh][i] = wh[i * 4:i * 4 + 4]
        return colliders

if __name__ == "__main__":

    TILESIZE = (16, 16)
    SCALEFACTOR = 30
    WIDTH = (TILESIZE[0]) * SCALEFACTOR
    HEIGHT = (TILESIZE[1]) * SCALEFACTOR
    SIZE = (WIDTH,HEIGHT)
    FPS = 30
    CLOCK = pygame.time.Clock()

    if len(sys.argv) > 1:
        texturefile = sys.argv[1]
        filename = texturefile[:texturefile.find('.')]
        texture = pygame.image.load(texturefile).convert_alpha()
        