import pygame
import random
import math

def get_center(surface):
	return surface.get_rect().center

class Cloud():
	def __init__(self, x, y):
		self.rotation = random.randint(0,360)
		self.rotVel = random.randint(-3,3)
		self.xvel = random.random()*random.randint(-1,1)
		self.yvel = random.random()*random.randint(-1,1)
		self.surf = pygame.image.load("cloud.png").convert_alpha()
		self.x = x
		self.y = y
		self.decay = random.randint(0, 256)
		#~ self.decay = 255
		self.subSurf = pygame.Surface((self.surf.get_size()), flags=pygame.SRCALPHA)
		#~ self.subSurf.fill((0,0,0,self.decay))
		self.subSurf.fill((0,0,0,5))
		self.surf.blit(self.subSurf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
		#~ self.subSurf.fill((0,0,0,5))
	
	def drawCloud(self, screen):
		self.surf.blit(self.subSurf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
		rotatedCloud = pygame.transform.rotate(self.surf, self.rotation)
		middle = get_center(rotatedCloud)
		screen.blit(rotatedCloud, (self.x-middle[0], self.y-middle[1]))
		self.x += self.xvel
		self.y += self.yvel
		self.rotation -= self.rotVel
		self.decay -= 5

class CloudGroup():
	def __init__(self, x, y, puffs=25, size=64):
		self.x = x
		self.y = y
		self.size = size
		self.clouds = []
		for i in range(puffs):
			self.clouds.append(Cloud(self.x+random.randint(-self.size,self.size), self.y+random.randint(-self.size,self.size)))
			#print "cloud # " + str(i)
	
	def drawClouds(self, screen):
		for i in range(len(self.clouds)):
			self.clouds[i].drawCloud(screen)
			if self.clouds[i].decay <= 0:
				#print "making new cloud..."
				del self.clouds[i]
				self.clouds.insert(i, Cloud(self.x+random.randint(-self.size,self.size), self.y+random.randint(-self.size,self.size)))
				
	def scroll(self, dx=0, dy=0):
		self.x = self.x + dx
		self.y = self.y + dy
		for i in range(len(self.clouds)):
			self.clouds[i].x = self.clouds[i].x + dx
			self.clouds[i].y = self.clouds[i].y + dy

class Wheel():
	def __init__(self, (x, y), rot=0, rotVel=-1):
		self.x = x
		self.y = y
		self.rot = rot
		self.rotVel = rotVel
		self.surf = pygame.image.load("wheel.png").convert_alpha()
	
	def rotated(self):
		rotatedWheel = pygame.transform.rotate(pygame.transform.flip(self.surf, True, False), self.rot)
		x,y = rotatedWheel.get_rect().center
		self.rot+=self.rotVel
		return rotatedWheel,x,y

class Ship():
	def __init__(self, x, y, rotPoint=(126,106)):
		self.surf = pygame.image.load("airship.png").convert_alpha()
		self.x = x - self.surf.get_width()/2
		self.y = y - self.surf.get_height()/2
		self.rotPoint = rotPoint
		self.offset = 0.0
		self.wheel = Wheel(rotPoint)
	
	def drawShip(self, screen):
		screen.blit(self.surf, (self.x, self.y+(16*math.sin(self.offset))))
		rotated,wx,wy = self.wheel.rotated()
		screen.blit(rotated, (self.x+self.rotPoint[0]-wx, self.y+self.rotPoint[1]-wy+(16*math.sin(self.offset))))
		self.offset = self.offset + .1
		

if __name__ == "__main__":
	
	pygame.mixer.init()
	
	WIDTH = 1024
	HEIGHT = 1024
	SIZE = (WIDTH,HEIGHT)
	FPS = 20
	fpsClock = pygame.time.Clock()
		
	SCREEN = pygame.display.set_mode(SIZE)
	pygame.display.set_caption('Of The Airship Academy')
	manycloudgroups = []
	for i in range(7):
		manycloudgroups.append(CloudGroup(random.randint(-200,WIDTH+200), random.randint(-200,HEIGHT+200)))
	
	ship = Ship(WIDTH/2, HEIGHT/2)
	
	pygame.mixer.music.load("Of The Airship Academy.mp3")
	pygame.mixer.music.play(-1, 1)
	
	blackness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert()
	trans = 255.0
	
	while True:
		
		for event in pygame.event.get():
			pass
		
		
		SCREEN.fill((133, 139, 255))
		
		for i in range(len(manycloudgroups)/2):
			manycloudgroups[i].drawClouds(SCREEN)
			manycloudgroups[i].scroll(-2)
			if manycloudgroups[i].x < -200:
				del manycloudgroups[i]
				manycloudgroups.insert(i, CloudGroup(WIDTH + 100 + random.randint(0,100), random.randint(0,HEIGHT)))

		ship.drawShip(SCREEN)

		for i in range(len(manycloudgroups)/2, len(manycloudgroups)):
			manycloudgroups[i].drawClouds(SCREEN)
			manycloudgroups[i].scroll(-4)
			if manycloudgroups[i].x < -200:
				del manycloudgroups[i]
				manycloudgroups.insert(i, CloudGroup(WIDTH + 100 + random.randint(0,100), random.randint(0,HEIGHT)))
		
		
		
		if trans > 0:
			SCREEN.blit(blackness, (0,0))
			trans-=.5
			blackness.set_alpha(trans)
		
		pygame.display.update()
		fpsClock.tick(FPS)
