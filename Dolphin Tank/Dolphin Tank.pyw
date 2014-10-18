import pygame, sys, time, random, math

def randomColor(R = None, G = None, B = None, Rmax = 255, Rmin = 0, Bmax = 255, Bmin = 0, Gmax = 255, Gmin = 0,):
	if R == None:
		R = random.randint(Rmin,Rmax)
	if G == None:
		G = random.randint(Gmin,Gmax)
	if B == None:
		B = random.randint(Bmin,Bmax)
	return (R, G, B)

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

def getNewColor():
	return randomColor(B = 255, Rmax = 50, Gmax = 100)

class Orb():
	def __init__(self, (x, y), radius, color = None, numOrbiters = None, orbiterRadius = None, orbiterDist = None, orbiterSpeed = None, xvel = None, yvel = None):
		self.x = x
		self.y = y
		self.center = (x, y)
		self.radius = radius
		
		self.color = color
		if color == None:
			self.color = getNewColor()
		assert len(self.color) == 3
		self.targetColor = getNewColor()
		
		self.xvel = xvel
		self.yvel = yvel
		if self.xvel == None and self.yvel == None:
			self.xvel = 0
			self.yvel = 0
			while (self.xvel,self.yvel) == (0,0):
				self.xvel = random.randint(-8,8)
				self.yvel = random.randint(-8,8)
			
		self.numOrbiters = numOrbiters
		if self.numOrbiters == None:
			self.numOrbiters = random.randint(5,10)
			
		self.orbiters = []
		
		for i in range(self.numOrbiters):
			rad = orbiterRadius
			distance = orbiterDist
			if rad == None:
				rad = random.randint(1,self.radius/4)
			if distance == None:
				distance = random.randint(self.radius, 2*self.radius)
			self.orbiters.append(Orbiter(self.center, rad, distance))
		
		self.orbiterSpacing = (2*math.pi)/self.numOrbiters
		self.orbitCycle = 0
		
		self.orbiterSpeed = orbiterSpeed
		if self.orbiterSpeed == None:
			direction = 0
			while direction == 0:
				direction = random.randint(-1,1)
			self.orbiterSpeed = (random.random()/6)*direction
	
	def draw(self, screen):
		#~ print self.color
		pygame.draw.circle(screen, self.color, self.center, self.radius)
		if self.color == self.targetColor:
			self.targetColor = getNewColor()
		else:
			self.color = adjustColorTo(self.targetColor, self.color)
			
		for i in range(len(self.orbiters)):
			theta = i*self.orbiterSpacing+self.orbitCycle
			x = int(self.orbiters[i].distance*math.sin(theta) + self.x)
			y = int(self.orbiters[i].distance*math.cos(theta) + self.y)
			self.orbiters[i].draw(screen, (x,y))
		self.orbitCycle+=self.orbiterSpeed
		if self.orbitCycle > 2*math.pi:
			self.orbitCycle = 0
		self.x+=self.xvel
		self.y+=self.yvel
		self.center = (self.x,self.y)
				

class Orbiter():
	def __init__(self, (x, y), radius, distance, color = None):
		self.center = (x, y)
		self.radius = radius
		self.distance = distance
		self.color = color
		if self.color == None:
			self.color = getNewColor()
		assert len(self.color) == 3
		self.targetColor = getNewColor()
	
	def draw(self, screen, (x,y)):
		pygame.draw.circle(screen, self.color, (x,y), self.radius)
		if self.color == self.targetColor:
			self.targetColor = getNewColor()
		else:
			self.color = adjustColorTo(self.targetColor, self.color)
		

def main():
	
	pygame.mixer.init()
	
	WIDTH = 512
	HEIGHT = 512
	SIZE = (WIDTH,HEIGHT)
	FPS = 60
	SCREEN = pygame.display.set_mode(SIZE)
	pygame.display.set_caption("Dolphin Tank")
	CLOCK = pygame.time.Clock()
	backgroundColor = getNewColor()
	targetColor = getNewColor()
	
	pygame.mixer.music.load("01-01- In the Dolphin Tank.mp3")
	pygame.mixer.music.play(-1)
	
	blobs = []
	for i in range(random.randint(10,30)):
		x = random.randint(-WIDTH, 2*WIDTH)
		y = random.randint(-HEIGHT, 2*HEIGHT)
		blobs.append(Orb((x,y), random.randint(8,64)))
		
	while True:
		
		if backgroundColor == targetColor:
			targetColor = getNewColor()
		else:
			backgroundColor = adjustColorTo(targetColor, backgroundColor)
		
		SCREEN.fill(backgroundColor)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
		replacelist = []
		for i in range(len(blobs)):
			blobs[i].draw(SCREEN)
			if blobs[i].x > WIDTH+blobs[i].radius or blobs[i].x < -blobs[i].radius:
				
				replacelist.append(i)
			elif blobs[i].y > HEIGHT+blobs[i].radius or blobs[i].y < -blobs[i].radius:
				replacelist.append(i)
		for each in replacelist:
			radius = blobs[each].radius
			section = random.randint(0,3)
			if section == 0:
				x = random.randint(WIDTH+radius, 2*WIDTH)
				y = random.randint(0, HEIGHT)
			elif section == 1:
				x = random.randint(0, WIDTH)
				y = random.randint(HEIGHT+radius, 2*HEIGHT)
			elif section == 2:
				x = random.randint(-WIDTH, -radius)
				y = random.randint(0, HEIGHT)
			elif section == 3:
				x = random.randint(0, WIDTH)
				y = random.randint(-HEIGHT, -radius)
			del blobs[each]
			blobs.insert(each, Orb((x, y), random.randint(8, 64)))
				
		

		pygame.display.update()
		CLOCK.tick(FPS)


if __name__ == "__main__":
	main()
