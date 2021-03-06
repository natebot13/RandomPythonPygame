import pygame
import sys
import random

def randomColor():
    color = (random.choice(range(0,256)), random.choice(range(0,256)), random.choice(range(0,256)))
    return color

class Land:
    def __init__(self, x, y, width, height, color, spawn = False):
        self.rect = pygame.Rect((x, y), (width, height))
        self.color = color
        if self.color == (0,0,0):
            self.collides = True
        else:
            self.collides = False
        self.spawn = spawn
    def flip(self):
        if self.color == (0,0,0):
            self.color = (255,255,255)
            self.collides = False
        else:
            self.color = (0,0,0)
            self.collides = True
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def loadLand(width, height, locations):
        lands = []
        landheight = height/len(locations)
        for y, each in enumerate(locations):
            landwidth = width/len(each)
            for x, pos in enumerate(each):
                if pos == 'S':
                    lands.append(Land(x*landwidth, y*landheight, landwidth, landheight, (255,255,255), True))
                if pos == 'O':
                    lands.append(Land(x*landwidth, y*landheight, landwidth, landheight, (255,255,255)))
                if pos == '%':
                    lands.append(Land(x*landwidth, y*landheight, landwidth, landheight, (0,0,0)))
                if pos == 'X':
                    lands.append(BlackLand(x*landwidth, y*landheight, landwidth, landheight, (0,0,0)))
        return lands

class BlackLand(Land):
    def flip(self):
        pass

class Character:
    def __init__(self, x, y, SCREENSIZE):
        self.SCREENSIZE = SCREENSIZE
        self.frame = 0
        self.direction = 0
        self.image = {}
        self.elapsed = 0
        self.falling = True
        self.jumping = False
        self.canjump = True
        self.fallspeed = 0
        self.xvel = 0
        self.yvel = 0
        for i in range(4):
            for j in range(2):
                self.image[str(i) + str(j)] = pygame.image.load('data/images/character' + str(i) + str(j) + '.png').convert_alpha()
        for i in range(4):
            self.image['jump' + str(i)] = pygame.image.load('data/images/characterjump' + str(i) + '.png')
        self.rect = pygame.Rect((x,y),self.image['00'].get_size())

    def draw(self, screen):
        if self.falling:
            screen.blit(self.image['jump' + str(self.direction)], self.rect)
        else:
            screen.blit(self.image[str(self.direction) + str(self.frame)], self.rect)

    def update(self, delta, terrain):
        dx = .4*self.xvel*delta
        dy = .4*self.yvel*delta

        # WALKING ANIMATION
        self.elapsed += delta
        if self.elapsed > 200 and self.walking:
            self.elapsed = 0
            if self.frame == 0:
                self.frame = 1
            else:
                self.frame = 0
        if not self.walking:
            self.frame = 0
        # END WALKING ANIMATION

        # CHECKING SPRITE IS WITHIN THE SCREEN
        if self.rect.left + dx < 0 and dx < 0:
            dx = 0
        if self.rect.right + dx > self.SCREENSIZE[0] and dx > 0:
            return True
        if self.rect.top + dy < 0 and dy < 0:
            dy = 0
        if self.rect.bottom + dy > self.SCREENSIZE[1] and dy > 0:
            dy = 0
        # END CHECKING

        # CHECKING FOR BLOCK COLLISION
        collisionlist = self.rect.collidelistall(terrain)
        print(collisionlist)
        if collisionlist:
            for each in collisionlist:
                if self.rect.bottom > terrain[each].top:
                    self.falling = False
        else:
            self.falling = True
        # END BLOCK COLLISION


        if self.falling:
            dy = self.fallspeed*delta*.004
            self.fallspeed += .5*delta
        else:
            self.fallspeed = 4
        self.rect.x += dx
        self.rect.y += dy

def loadlvlfromfile(filename):
    level = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            level.append(list(line))
    return level

def getspawnblock(terrain):
    i = 0
    for each in terrain:
        if each.spawn:
            return each
    raise ValueError('No spawn block')

def getsolidterrain(terrain):
    rectlist = [block.rect for block in terrain if block.collides]
    return rectlist

def main():

    pygame.mixer.init()
    
    # WIDTH = 512
    # HEIGHT = 512
    # SIZE = (WIDTH,HEIGHT)
    FPS = 60
    SCREEN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    SIZE = SCREEN.get_size()
    WIDTH, HEIGHT = SIZE[0], SIZE[1]
    pygame.display.set_caption("Awesome Game!")
    CLOCK = pygame.time.Clock()
    keys = {'left': False, 'right': False, 'up': False, 'down': False}
    left, right, up, down = 0, 0, 0, 0

    levelnum = 0
    terrain = Land.loadLand(WIDTH, HEIGHT, loadlvlfromfile('data/levels/level' + str(levelnum)))
    spawnblock = getspawnblock(terrain)
    character = Character(spawnblock.rect.x, spawnblock.rect.y, SIZE)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    keys['right'] = True
                    character.direction = 0
                    right = 1
                if event.key == pygame.K_LEFT:
                    keys['left'] = True
                    character.direction = 2
                    left = -1
                if event.key == pygame.K_UP:
                    keys['up'] = True
                    character.direction = 1
                    up = -1
                if event.key == pygame.K_DOWN:
                    keys['down'] = True
                    character.direction = 3
                    down = 1
                if event.key == pygame.K_SPACE and character.canjump:
                    character.fallspeed = -100
                    character.jumping = True
                if event.key == pygame.K_f:
                    for each in terrain:
                        each.flip()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    keys['right'] = False
                    right = 0
                if event.key == pygame.K_LEFT:
                    keys['left'] = False
                    left = 0
                if event.key == pygame.K_UP:
                    keys['up'] = False
                    up = 0
                if event.key == pygame.K_DOWN:
                    keys['down'] = False
                    down = 0
                if event.key == pygame.K_SPACE:
                    character.jumping = False

        if keys['left'] or keys['right'] or keys['up'] or keys['down']:
            if keys['left'] and keys['right'] or keys['up'] and keys['down']:
                character.walking = False
            else:
                character.walking = True
        else:
            character.walking = False

        SCREEN.fill((100,100,100))
        delta = CLOCK.get_time()
        
        for block in terrain:
            block.draw(SCREEN)

        character.xvel = left + right
        character.yvel = up + down

        nextlevel = character.update(delta, getsolidterrain(terrain))
        if nextlevel:
            levelnum += 1
            del terrain
            del spawnblock
            del character
            terrain = Land.loadLand(WIDTH, HEIGHT, loadlvlfromfile('data/levels/level' + str(levelnum)))
            spawnblock = getspawnblock(terrain)
            character = Character(spawnblock.rect.x, spawnblock.rect.y, SIZE)


        character.draw(SCREEN)

        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main()