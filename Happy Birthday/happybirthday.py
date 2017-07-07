import pygame, datetime, random, os, sys
pygame.mixer.init()
pygame.font.init()

def randomColor():
	return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def adjustColorTo(targetColor, currentColor, amount=1):
	nextColor = []
	for i in range(3):
		if currentColor[i] > targetColor[i]:
			nextColor.append(currentColor[i]-amount)
		elif currentColor[i] < targetColor[i]:
			nextColor.append(currentColor[i]+amount)
		elif currentColor[i] == targetColor[i]:
			nextColor.append(currentColor[i])
	return tuple(nextColor)

class Explosion():
	def __init__(self, x, y, mag=50, fuzelen = 120):
		self.x = x
		self.y = y
		self.fuse = random.randint(0, fuzelen)
		self.done = False
		self.parts = []
		self.sound = pygame.mixer.Sound(file=os.getcwd() + "/sounds/" + random.choice(os.listdir("sounds")))
		self.played = False
		for i in range(mag):
			self.parts.append(Particle(self.x,self.y))
	
	def draw(self, screen):
		if self.fuse <= 0:
			if self.played == False:
				self.sound.play()
				self.played = True
			self.done = True
			for i in range(len(self.parts)-1, -1, -1):
				self.parts[i].draw(screen)
				if self.parts[i].done == False:
					self.done = False
				else:
					del self.parts[i]
		else:
			self.fuse-=1
			
class Particle():
	def __init__(self, x, y, radius=2, lifemax=60, maxvel=30):
		self.x = x
		self.y = y
		self.radius = radius
		self.life = random.randint(0,lifemax)
		self.color = randomColor()
		self.done = False
		self.dx = random.randint(-maxvel,maxvel)
		self.dy = random.randint(-maxvel,maxvel)
	
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
		self.x+=self.dx
		self.y+=self.dy
		self.life-=1
		if self.life <= 0:
			self.done = True

def main():
	
	SCREEN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	WIDTH, HEIGHT = SCREEN.get_size()
	
	FPS = 60.0
	CLOCK = pygame.time.Clock()
	
	dy = 0
	
	fontfile = pygame.font.get_default_font()
	FONT2015 = pygame.font.Font(fontfile, 128)
	
	countdownDone = True
	expNum = 10

	explos = []
	for i in range(expNum):
		explos.append(Explosion(random.randint(0,WIDTH), random.randint(0,HEIGHT)))
	
	while countdownDone:
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
		
		SCREEN.fill(randomColor())
		
		for i in range(len(explos)-1,-1,-1):
			if explos[i].done == True:
				explos[i] = Explosion(random.randint(0,WIDTH), random.randint(0,HEIGHT))
			else:
				explos[i].draw(SCREEN)
		
		newYear = FONT2015.render("Happy 13th Birthday!", True, randomColor())
		SCREEN.blit(newYear, (WIDTH/2-newYear.get_width()/2, HEIGHT/2-newYear.get_height()/2))
		
		pygame.display.update()
		CLOCK.tick(FPS)

if __name__ == "__main__":
	main()
