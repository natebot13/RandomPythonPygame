import pygame, os, Components

class MapManager():
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
            exits = tuple(f.readline().split(','))
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
                            roomx = tilex * self.tilesize[0]
                            roomy = tiley * self.tilesize[1]
                            collider = None
                            if tilenum in self.collisionRects:
                                for each in self.collisionRects[tilenum]:
                                    collider = each.move(roomx, roomy)
                                    collManager.insertCollider(collider)
                            if layernames[len(tiles)].lower() == 'entities':
                                self.roomColliderEntity(self.surf.subsurface(pygame.Rect((x, y), self.tilesize)), roomx, roomy, collManager.scalefactor, entManager, collider)
                            elif layernames[len(tiles)].lower() == 'tops':
                                self.roomTopEntity(self.surf.subsurface(pygame.Rect((x, y), self.tilesize)), roomx, roomy, collManager.scalefactor, entManager)
                            else:
                                tiles.append(self.surf.subsurface(pygame.Rect((x, y), self.tilesize)))
                        else:
                            tiles.append(None)
                    surfArray.append(tiles)
                    tilex += 1
                tiley += 1
                    
        return Room(roomsize, self.tilesize, exits, surfArray)

    def loadColliders(self, collidersfile):
        colliders = {}
        with open(os.path.join('colliders', collidersfile)) as f:
            for line in f:
                numwh = line.split(':')
                wh = numwh[1].split(',')
                colliders[int(numwh[0])] = []
                for i in range(len(wh)//4):
                    colliders[int(numwh[0])].append(pygame.Rect(int(wh[0]), int(wh[1]), int(wh[2]), int(wh[3])))
        return colliders

    def roomColliderEntity(self, surface, x, y, scalefactor, entManager, collider = None):
        ID = entManager.newEntity()
        if collider:
            entManager.addComponentToEntity(ID, Components.Collider(collider))
        entManager.addComponentToEntity(ID, Components.Renderable(scalefactor, None, surface))
        entManager.addComponentToEntity(ID, Components.Position(x * scalefactor, y * scalefactor))

    def roomTopEntity(self, surface, x, y, scalefactor, entManager):
        ID = entManager.newEntity()
        entManager.addComponentToEntity(ID, Components.Renderable(scalefactor, None, surface))
        entManager.addComponentToEntity(ID, Components.Position(x * scalefactor, y * scalefactor))
        entManager.addComponentToEntity(ID, Components.Top())

class Room():
    def __init__(self, size, tilesize, exits, surfArray):
        self.size = size
        self.tilesize = tilesize
        self.width, self.height = size
        self.width = int(self.width)
        self.height = int(self.height)
        self.up, self.right, self.down, self.left = exits
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