import pygame
import os, sys
import EntityManager, Components, Systems

class Map():
    def __init__(self, texture, colliders, tilesize=(16,16)):
        self.surf = pygame.image.load(os.path.join("textures", texture)).convert_alpha()
        # self.collisionRects = loadColiders(colliders)
        self.tilesize = tilesize
        w, h = tilesize
        r = self.surf.get_rect()
        self.xTiles = r.width / w
        self.yTiles = r.height / h
        self.room = None

    def loadRoom(self, roomname):
        with open(os.path.join("rooms", roomname + ".room")) as f:
            roomsize = tuple(f.readline().split(","))
            dirs = tuple(f.readline().split(","))
            surfArray = []
            roomColliders = []
            for line in f:
                for layers in line.split(","):
                    tiles = []
                    for tilenum in layers.split("|"):
                        tilenum = int(tilenum)
                        tilenum -= 1
                        if tilenum >= 0:
                            x = (tilenum % self.xTiles) * self.tilesize[0]
                            y = (tilenum // self.xTiles) * self.tilesize[1]
                            # roomColliders.append(self.collisionRects[tilenum].move(x, y))
                            tiles.append(self.surf.subsurface(pygame.Rect((x, y),self.tilesize)))
                        else:
                            tiles.append(None)
                    surfArray.append(tiles)
                    
        return Room(roomsize, self.tilesize, dirs, surfArray, roomColliders)

class Room():
    def __init__(self, size, tilesize, dirs, surfArray, roomColliders):
        self.size = size
        self.tilesize = tilesize
        self.width, self.height = size
        self.width = int(self.width)
        self.height = int(self.height)
        self.up, self.right, self.down, self.left = dirs
        self.room = surfArray
        self.roomColliders = roomColliders

    def draw(self, screen):
        w, h = self.tilesize
        xpos, ypos = 0, 0
        for each in self.room:
            for tile in each:
                if tile != None:
                    screen.blit(tile, (xpos * w, ypos * h))
            if xpos < self.width - 1:
                xpos += 1
            else:
                ypos += 1
                xpos = 0

if __name__ == "__main__":
    
    pygame.mixer.init()
    
    NUMTILES = (16, 16)
    TILESIZE = (16, 16)
    SMALLSIZE = (NUMTILES[0] * TILESIZE[0], NUMTILES[1] * TILESIZE[1])
    WIDTH = SMALLSIZE[0] * 3
    HEIGHT = SMALLSIZE[1] * 3
    SIZE = (WIDTH,HEIGHT)
    FPS = 30
    CLOCK = pygame.time.Clock()
        
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Nate\'s RPG')

    entManager = EntityManager.EntityManager()
    sysManager = Systems.SystemsManager(entManager, SCREEN)
    ID = entManager.newEntity()
    entManager.addComponentToEntity(ID, Components.Position(100, 100))
    entManager.addComponentToEntity(ID, Components.Velocity())
    entManager.addComponentToEntity(ID, Components.Renderable('boy/boy_blue.png'))
    entManager.addComponentToEntity(ID, Components.Controllable([pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]))

    m = Map("blowharderterrain.png", "blowhardercolliders.col", TILESIZE)
    room = m.loadRoom("titlescreen")
    # room.addCharacter("")
    smallscreen = pygame.Surface(SMALLSIZE)

    while True:
        
        SCREEN.fill((0, 0, 0))
        room.draw(smallscreen)
        pygame.transform.scale(smallscreen, SCREEN.get_rect().size, SCREEN)
        sysManager.runSystems(CLOCK.get_time())
        sysManager.endStep()
        pygame.display.update()
        CLOCK.tick(FPS)