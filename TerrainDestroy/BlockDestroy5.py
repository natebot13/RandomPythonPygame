import pygame, random, scipy#, pymunk
import pygame.gfxdraw

def randomColor():
	color = (random.choice(range(0,256)), random.choice(range(0,256)), random.choice(range(0,256)))
	return color

class block():
	def __init__(self, rect, color=0):
		self.rect = rect
		if color == 0:
			#self.color = (100,50,0)
			self.color = randomColor()
		else:
			self.color = color

class blockDestroy():
	def __init__(self, location=((0,0),(512,512)), smallest=4):
		pygame.init()
		
		self.SIZE = location[1]
		self.SMALLEST = smallest

		self.terrain = [block(pygame.Rect(location), (0,0,0))]
		self.mousepos = None
	
	def getClickedPoint(self):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEMOTION:
				#print "I've been clicked!"
				self.mousepos = event.pos
				return event.pos
		return None

	def sizeOfPeice(self, point):
		#print "Checking size of peice"
		for block in self.terrain:
			if block.rect.collidepoint(point):
				return block.rect.size

	def splitBlocks(self, point):
		#print "Splitting blocks"
		splitthese = []
		for i in range(0, len(self.terrain)):
			#print self.terrain
			if self.terrain[i].rect.collidepoint(point):
				splitthese.append(i)
		splitthese.reverse()
		for i in splitthese:	
			position = (self.terrain[i].rect.topleft, self.terrain[i].rect.size)
			del self.terrain[i]
			newWH = (position[1][0]/2, position[1][1]/2)
			newCoords = [(position[0][0], position[0][1]),
						(position[0][0]+newWH[0], position[0][1]),
						(position[0][0], position[0][1]+newWH[1]),
						(position[0][0]+newWH[0], position[0][1]+newWH[1])]
			for j in range(3,-1,-1):
				newrect = pygame.Rect(newCoords[j],newWH)
				R = (255-newrect.size[1]*5)/2 + (abs(255-newrect.size[1]*5))/2 + 1
				G = (127-newrect.size[1]*5)/2 + (abs(127-newrect.size[1]*5))/2 + 1
				blockcolor = (R,G,0)
				#print blockcolor
				self.terrain.insert(i, block(newrect, blockcolor))
				#self.terrain.insert(i, block(newrect))
				#print self.terrain
	
	def removePeice(self, point):
		removelist = []
		for i in range(0, len(self.terrain)):
			if self.terrain[i].rect.collidepoint(point):
				removelist.append(i)
		removelist.reverse()
		for i in removelist:
			del self.terrain[i]

	def destroyPeice(self, point):
		#print "Destroying peice at: " + str(point)
		peiceremoved = False
		while peiceremoved == False:
			if self.sizeOfPeice(point) > (self.SMALLEST, self.SMALLEST):
				self.splitBlocks(point)
			else:
				self.removePeice(point)
				peiceremoved = True
	
	def drawTerrain(self, screen):
		for i in range(0, len(self.terrain)):
			pygame.gfxdraw.box(screen, self.terrain[i].rect, self.terrain[i].color)
			#pygame.draw.rect(screen, self.terrain[i].color, self.terrain[i].rect)
	
	def removeSmallParts(self):
		deletelist = []
		for i in range(0, len(self.terrain)):
			print i
			if self.terrain[i].size < (self.SMALLEST, self.SMALLEST):
				deletelist.append(i)
		for i in deletelist.reverse():
			del self.terrain[i]

if __name__ == "__main__":

	AIRSPACE = 100
	WIDTH = 512
	HEIGHT = WIDTH + AIRSPACE
	SIZE = (WIDTH,HEIGHT)
	TERRAINSIZE = (WIDTH,WIDTH)
	FPS = 60
	fpsClock = pygame.time.Clock()
		
	SCREEN = pygame.display.set_mode(SIZE)
	pygame.display.set_caption('Terrain Test')
	
	undergroundambience = location=((0,AIRSPACE),TERRAINSIZE)
	
	bd = blockDestroy(location=((0,AIRSPACE),TERRAINSIZE), smallest=1)
	while True:
		mousepos = bd.getClickedPoint()
		if mousepos != None:
			bd.destroyPeice(mousepos)
		
		SCREEN.fill((150,150,150))
		pygame.gfxdraw.box(SCREEN, undergroundambience, (25,25,25))
		bd.drawTerrain(SCREEN)
		
		pygame.display.update()
		fpsClock.tick(FPS)
