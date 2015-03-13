import pygame, sys, os, math, random

def randomColor(R = None, G = None, B = None, Rmax = 255, Rmin = 0, Bmax = 255, Bmin = 0, Gmax = 255, Gmin = 0,):
    if R == None:
        R = random.randint(Rmin,Rmax)
    if G == None:
        G = random.randint(Gmin,Gmax)
    if B == None:
        B = random.randint(Bmin,Bmax)
    return (R, G, B)

class Particle():
    def __init__(self, (x,y), radius=None, color=None, hilf=False):
        self.x = x
        self.y = y
        self.xvel = random.randint(-20, 20)
        self.radius = radius
        self.image = pygame.image.load(os.path.join(os.getcwd(), 'ball.png'))
        if random.randint(0,1000) == 0 or hilf:
            self.image = pygame.image.load(os.path.join(os.getcwd(), 'hilf.png'))
        if self.radius == None:
            self.radius = random.randint(1,5)
        self.center = (x,y)
        self.color = color
        if self.color == None:
            pass
            # self.color = randomColor(R = 255, B = 0, Gmin = 0)
            # self.color = (255,255,255,255)
        self.t = -40 + random.randint(-5,5)
            
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        # pygame.draw.circle(screen, self.color, (int(self.x),int(self.y)), self.radius)
        self.t+=1

def main():
    # WIDTH = 1500
    # HEIGHT = 800
    # SIZE = (WIDTH, HEIGHT)
    SCREEN = pygame.display.set_mode()
    WIDTH = SCREEN.get_width()
    HEIGHT = SCREEN.get_height()
    FPS = 30
    CLOCK = pygame.time.Clock()
    
    xvel = 0
    yvel = -1
    counter = 0
    particles = []
    
    while True:
        
        SCREEN.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    particles.append(Particle((random.randint(0,WIDTH), HEIGHT), hilf=True))

        if counter == 0:
            particles.append(Particle((random.randint(0,WIDTH), HEIGHT)))
            counter = 0
        else:
            counter += 1
        dellist = []
        for i in range(len(particles)):
            particles[i].y-=yvel*particles[i].t
            particles[i].x+=particles[i].xvel
            if particles[i].y < 0 or particles[i].y > HEIGHT+10:
                dellist.append(i)
            particles[i].draw(SCREEN)
        dellist.reverse()
        for each in dellist:
            del particles[each]
        
        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
