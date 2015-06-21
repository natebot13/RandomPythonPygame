import pygame
import os, sys
import EntityManager, SystemsManager, ColliderManager, Components, Systems

class Map():
    def __init__(self, texturefile, collidersfile, tilesize=(16,16)):
        self.surf = pygame.image.load(os.path.join("textures", texturefile)).convert_alpha()
        self.collisionRects = self.loadColliders(collidersfile)
        self.tilesize = tilesize
        w, h = tilesize
        r = self.surf.get_rect()
        self.xTiles = r.width / w
        self.yTiles = r.height / h
        self.room = None

    def loadRoom(self, roomname, entManager, collManager):
        with open(os.path.join('rooms', roomname + '.room')) as f:
            roomsize = tuple(f.readline().split(','))
            dirs = tuple(f.readline().split(','))
            layernames = tuple(f.readline().split(','))
            surfArray = []

            tiley = 0
            for line in f:
                tilex = 0
                for layers in line.split(','):
                    tiles = []
                    for tilenum in layers.split('|'):
                        tilenum = int(tilenum)
                        tilenum -= 1
                        if tilenum >= 0:
                            x = (tilenum % self.xTiles) * self.tilesize[0]
                            y = (tilenum // self.xTiles) * self.tilesize[1]
                            if layernames[len(tiles)].lower() == 'entities':
                                roomx = tilex * self.tilesize[0]
                                roomy = tiley * self.tilesize[1]
                                collider = None
                                if tilenum in self.collisionRects:
                                    collider = self.collisionRects[tilenum].move(roomx, roomy)
                                    collManager.insertCollider(collider)
                                self.roomEntity(self.surf.subsurface(pygame.Rect((x, y), self.tilesize)), roomx, roomy, collManager.scalefactor, entManager, collider)
                            else:
                                tiles.append(self.surf.subsurface(pygame.Rect((x, y), self.tilesize)))
                        else:
                            tiles.append(None)
                    surfArray.append(tiles)
                    tilex += 1
                tiley += 1
                    
        return Room(roomsize, self.tilesize, dirs, surfArray)

    def loadColliders(self, collidersfile):
        colliders = {}
        with open(os.path.join('colliders', collidersfile)) as f:
            for line in f:
                numwh = line.split(':')
                wh = numwh[1].split(',')
                colliders[int(numwh[0])] = pygame.Rect(int(wh[0]), int(wh[1]), int(wh[2]), int(wh[3]))
        return colliders

    def roomEntity(self, surface, x, y, scalefactor, entManager, collider = None):
        ID = entManager.newEntity()
        if collider:
            entManager.addComponentToEntity(ID, Components.Collider(collider))
        entManager.addComponentToEntity(ID, Components.Renderable(scalefactor, None, surface))
        entManager.addComponentToEntity(ID, Components.Position(x * scalefactor, y * scalefactor))

class Room():
    def __init__(self, size, tilesize, dirs, surfArray):
        self.size = size
        self.tilesize = tilesize
        self.width, self.height = size
        self.width = int(self.width)
        self.height = int(self.height)
        self.up, self.right, self.down, self.left = dirs
        self.room = surfArray

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

    def getColliders(self):
        return self.colliders

def main():    
    pygame.mixer.init()
    
    NUMTILES = (16, 16)
    TILESIZE = (16, 16)
    SMALLSIZE = (NUMTILES[0] * TILESIZE[0], NUMTILES[1] * TILESIZE[1])
    SCALEFACTOR = 3
    ENTITYSCALEFACTOR = 1.75
    WIDTH = SMALLSIZE[0] * SCALEFACTOR
    HEIGHT = SMALLSIZE[1] * SCALEFACTOR
    SIZE = (WIDTH,HEIGHT)
    FPS = 60
    CLOCK = pygame.time.Clock()

    pygame.display.set_caption("Nate's RPG")
    icon = pygame.image.load('textures/blue_n.png')
    icon.set_colorkey((0,255,0))
    pygame.display.set_icon(icon)
    SCREEN = pygame.display.set_mode(SIZE)

    entManager = EntityManager.EntityManager()
    sysManager = SystemsManager.SystemsManager(entManager)
    collManager = ColliderManager.ColliderManager(SCALEFACTOR, ENTITYSCALEFACTOR)

    m = Map("blowharderterrain.png", "blowharderterrain.col", TILESIZE)
    room = m.loadRoom("titlescreen", entManager, collManager)
    smallscreen = pygame.Surface(SMALLSIZE)

    sysManager.registerSystem(Systems.KeyboardInput())
    sysManager.registerSystem(Systems.Movable())
    sysManager.registerSystem(Systems.AnimateWhenMoving())
    sysManager.registerSystem(Systems.Multifaced())
    sysManager.registerSystem(Systems.Move(ENTITYSCALEFACTOR))
    sysManager.registerSystem(Systems.Collide(collManager))
    sysManager.registerSystem(Systems.SortByY(entManager))
    sysManager.registerSystem(Systems.Render(SCREEN))

    ID = entManager.newEntity()
    entManager.addComponentToEntity(ID, Components.Position(WIDTH/2, HEIGHT/2))
    entManager.addComponentToEntity(ID, Components.Velocity())
    entManager.addComponentToEntity(ID, Components.Collidable(pygame.Rect(4,8,8,8), ENTITYSCALEFACTOR))
    entManager.addComponentToEntity(ID, Components.Renderable(ENTITYSCALEFACTOR, 'boy/boy_blue.png'))
    entManager.addComponentToEntity(ID, Components.Animated())
    entManager.addComponentToEntity(ID, Components.Multifaced())
    entManager.addComponentToEntity(ID, Components.MovementAnimation())
    entManager.addComponentToEntity(ID, Components.Movable([pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s]))
    entManager.addComponentToEntity(ID, Components.Controllable([pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_SPACE]))

    while True:
        
        SCREEN.fill((0, 0, 0))
        room.draw(smallscreen)
        pygame.transform.scale(smallscreen, SCREEN.get_rect().size, SCREEN)
        sysManager.runSystems(CLOCK.get_time())
        sysManager.endStep()
        # for each in collManager.colliders:
        #     pygame.draw.rect(SCREEN, (255,0,0), each)
        CLOCK.tick(FPS)
        # print(CLOCK.get_fps())

if __name__ == "__main__":
    # import cProfile as profile
    # profile.run('main()')
    main()