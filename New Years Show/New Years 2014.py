import pygame, time, datetime, random
import pygame.camera
pygame.camera.init()

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
		self.wireframe = pygame.image.load("wireframe.png").convert_alpha()
		self.width = self.wireframe.get_width()
		self.height = self.wireframe.get_height()
		self.wireframe = pygame.transform.scale(self.wireframe, (self.width/4, self.height/4))
		self.width = self.wireframe.get_width()
		self.height = self.wireframe.get_height()
		self.center = (x,y)
		self.x = x - self.width/2
		self.y = y - self.height/2
		self.radius = self.width/2
		self.creationtime = time.localtime()
	
	def draw(self, screen, color):
		pygame.draw.ellipse(screen, color, self.wireframe.get_rect())
		screen.blit(self.wireframe, (self.x,self.y))

class Particle():
	def __init__(self, x, y, life):
		self.surf = pygame.image.load("particle.png")
		self.x = x - self.surf.get_width()/2
		self.y = y - self.surf.get_height()/2
		self.life = life

def main():
	SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	WIDTH = SCREEN.get_width()
	HEIGHT = SCREEN.get_height()
	FPS = 60.0
	CLOCK = pygame.time.Clock()
	
	track = pygame.Rect(WIDTH/2-8,0,16,HEIGHT)
	
	ball = Ball(WIDTH/2, 128)
	
	currentColor = randomColor()
	nextColor = randomColor()
	
	lenToGo = HEIGHT - 2*ball.radius
	timeToGo = datetime.datetime(2013, 12, 31, 3) - datetime.datetime.now()
	print str(timeToGo)
	
	dy = float(lenToGo)/(timeToGo.seconds*FPS)
	print dy
	
	while True:
		for event in pygame.event.get():
			pass
		
		if nextColor == currentColor:
			nextColor = randomColor()
		else:
			currentColor = adjustColorTo(nextColor, currentColor, 1)
		SCREEN.fill((0,0,0))
		pygame.draw.rect(SCREEN,(20,20,20),track)
		ball.draw(SCREEN, currentColor)
		ball.y += dy
		print ball.y
		pygame.display.update()
		CLOCK.tick(FPS)
		#print CLOCK.get_fps()
	

if __name__ == "__main__":
	main()
