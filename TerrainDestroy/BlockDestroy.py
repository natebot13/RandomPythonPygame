import pygame, random

class blockDestroy():
	def __init__(self):
		pygame.init()
		
		self.SIZE = (512,512)
		self.SMALLEST = 32
		self.FPS = 30
		self.fpsClock = pygame.time.Clock()
		
		self.SCREEN = pygame.display.set_mode(self.SIZE)
		pygame.display.set_caption('Terrain Test')

		self.terrain = [pygame.Rect((0,0),self.SIZE)]
		self.terrainColors = [self.randomColor()]
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
			if block.collidepoint(point):
				return block.size

	def splitBlocks(self, point):
		#print "Splitting blocks"
		for i in range(0, len(self.terrain)):
			#print self.terrain
			if self.terrain[i].collidepoint(point):
				position = (self.terrain[i].topleft, self.terrain[i].size)
				del self.terrain[i]
				del self.terrainColors[i]
				newWH = (position[1][0]/2, position[1][1]/2)
				newCoords = [(position[0][0], position[0][1]),
							(position[0][0]+newWH[0], position[0][1]),
							(position[0][0], position[0][1]+newWH[1]),
							(position[0][0]+newWH[0], position[0][1]+newWH[1])]
				for j in range(3,-1,-1):
					self.terrain.insert(i, pygame.Rect(newCoords[j],newWH))
					self.terrainColors.insert(i, self.randomColor())
				#~ self.terrain.insert(i, pygame.Rect(newCoords[2],newWH))
				#print self.terrain
	
	def removePeice(self, point):
		for i in range(0, len(self.terrain)-1):
			if self.terrain[i].collidepoint(point):
				del self.terrain[i]
				del self.terrainColors[i]

	def destroyPeice(self, point):
		#print "Destroying peice at: " + str(point)
		peiceremoved = False
		while peiceremoved == False:
			if self.sizeOfPeice(point) > (self.SMALLEST, self.SMALLEST):
				self.splitBlocks(point)
			else:
				self.removePeice(point)
				peiceremoved = True
				
	def randomColor(self):
		color = (random.choice(range(0,256)), random.choice(range(0,256)), random.choice(range(0,256)))
		return color
	
	def updateScreen(self):
		self.SCREEN.fill((0,0,0))
		for i in range(0, len(self.terrain)):
			pygame.draw.rect(self.SCREEN, self.terrainColors[i], self.terrain[i])
		pygame.display.update()
		self.fpsClock.tick(self.FPS)
	
	def removeSmallParts(self):
		deletelist = []
		for i in range(0, len(self.terrain)):
			print i
			if self.terrain[i].size < (self.SMALLEST, self.SMALLEST):
				deletelist.append(i)
		for i in range(0, len(deletelist)):
			del self.terrain[i]
			del self.terrainColors[i]

if __name__ == "__main__":
	bd = blockDestroy()
	while True:
		mousepos = bd.getClickedPoint()
		if mousepos != None:
			bd.destroyPeice(mousepos)
			bd.removeSmallParts()
		bd.updateScreen()
