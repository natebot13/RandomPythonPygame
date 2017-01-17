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

class Ball():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = pygame.image.load("wireframe.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.image.get_width()/4, self.image.get_height()/4))
		self.currentColor = randomColor()
		self.targetColor = randomColor()
	
	def draw(self, screen, dx=0, dy=0):
		pygame.draw.ellipse(screen, self.currentColor, ((self.x-self.image.get_width()/2,self.y-self.image.get_height()/2),self.image.get_size()))
		screen.blit(self.image, (self.x-(self.image.get_width()/2), self.y-(self.image.get_height()/2)))
		if self.currentColor == self.targetColor:
			self.targetColor = randomColor()
		else:
			self.currentColor = adjustColorTo(self.targetColor, self.currentColor)
		self.x += dx
		self.y += dy

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

class Photo():
	def __init__(self, imageloc, x, y, maxdegree=20, solidFor=120, transVel=1):
		self.x = x
		self.y = y
		self.trans = 0
		self.direction = transVel
		self.solidFor = solidFor
		self.done = False
		self.image = pygame.image.load(imageloc).convert()
		self.image.set_colorkey((1,1,1))
		self.image = pygame.transform.rotate(self.image, random.randint(-maxdegree, maxdegree))
		self.width, self.height = self.image.get_size()
		self.image.set_alpha(self.trans)
	
	def draw(self, screen):
		if self.done == False:
			screen.blit(self.image, (self.x-self.width/2, self.y-self.height/2))
			self.image.set_alpha(self.trans)
			if self.trans <= 255 and self.trans >= 0:
				self.trans+=self.direction
			else:
				if self.solidFor > 0:
					self.solidFor -=1
				else:
					self.direction = -self.direction
					self.trans += self.direction
			if self.trans <= 0 and self.solidFor <= 0:
				self.done = True



def main():
	
	beginDrop = 30
	finalDate = datetime.datetime(2015, 9, 19, 20, 54)
	expNum = 10
	
	SCREEN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	WIDTH, HEIGHT = SCREEN.get_size()
	
	FPS = 60.0
	CLOCK = pygame.time.Clock()
	
	ball = Ball(WIDTH/2, 128)
	
	track = pygame.Rect(WIDTH/2-8,0,16,HEIGHT)
	
	PTG = HEIGHT - ball.image.get_height()
	
	dy = 0
	
	fontfile = pygame.font.get_default_font()
	FONT = pygame.font.Font(fontfile, 64)
	FONT2015 = pygame.font.Font(fontfile, 256)
	
	countdownDone = False
	
	while not countdownDone:
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
		
		SCREEN.fill((0,0,0))
		
		pygame.draw.rect(SCREEN, (20,20,20), track)
		
		TTGdelta = (finalDate - datetime.datetime.now())
		
		if TTGdelta.seconds == beginDrop:
			TTG = TTGdelta.seconds*FPS
			dy = PTG/TTG
		if TTGdelta.days == -1:
			dy = 0
			countdownDone = True
		
		ball.draw(SCREEN, 0, dy)
				
		SCREEN.blit(FONT.render(str(TTGdelta)[:-3], True, (255,255,255)), (WIDTH-WIDTH/4, HEIGHT/2))
		
		pygame.display.update()
		CLOCK.tick(FPS)
		
	
	explos = []
	for i in range(expNum):
		explos.append(Explosion(random.randint(0,WIDTH), random.randint(0,HEIGHT)))
	
	images = []
	for name in os.listdir("photos"):
		if ".jpg" in name.lower():
			images.append(Photo(os.getcwd() + "/photos/" + name, random.randint(320, WIDTH-320), random.randint(320, HEIGHT-320), solidFor=2*FPS, transVel=5))
	currentPhoto = 0
	
	waitForPics = 5*FPS
	
	while countdownDone:
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
		
		SCREEN.fill((0,0,0))
		
		for i in range(len(explos)-1,-1,-1):
			if explos[i].done == True:
				explos[i] = Explosion(random.randint(0,WIDTH), random.randint(0,HEIGHT))
			else:
				explos[i].draw(SCREEN)
		
		pygame.draw.rect(SCREEN, (20,20,20), track)
		
		ball.draw(SCREEN, 0, dy)
		
		newYear = FONT2015.render("2015", True, randomColor())
		SCREEN.blit(newYear, (WIDTH/2-newYear.get_width()/2, HEIGHT/2-newYear.get_height()/2))
		
		if waitForPics <= 0:
			if currentPhoto < len(images):
				images[currentPhoto].draw(SCREEN)
				if images[currentPhoto].done == True:
					currentPhoto+=1
		else:
			waitForPics -= 1
		
		pygame.display.update()
		CLOCK.tick(FPS)

if __name__ == "__main__":
	main()
