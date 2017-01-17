import pygame, random
import pygame.gfxdraw

def randomColor():
	color = (random.choice(range(0,256)), random.choice(range(0,256)), random.choice(range(0,256)))
	return color

class block(pygame.Rect):
	def __init__(self, coorddata, color=None):
		super(block, self).__init__(coorddata[0][0],coorddata[0][1],coorddata[1][0],coorddata[1][1])
		self.removed = False
		if color == None:
			self.color = (100,50,0)
			# self.color = randomColor()
		else:
			self.color = color

class DestructibleTerrain():
	def __init__(self, startingblock=((0,0),(512,512)), smallest = 4):
		self.SMALLEST = smallest
		#print "Created the starting block!"
		self.terrain = [block(startingblock)]
		#print self.terrain

	def destroyTerrainAt(self, rect):
		collisions = rect.collidelistall(self.terrain)
		collisions.sort()
		collisions.reverse()
		for index in collisions:
			if self.terrain[index].size > (self.SMALLEST, self.SMALLEST):
				#print "Splitting..."
				self.splitBlock(index)
			else:
				#print "Marking for removal"
				self.terrain[index].removed = True
		self.cleanupTerrain()

	def splitBlock(self, index):
		position = (self.terrain[index].topleft, self.terrain[index].size)
		newWH = (position[1][0]/2, position[1][1]/2)
		newCoords = [(position[0][0]+newWH[0], position[0][1]+newWH[1]),
					(position[0][0], position[0][1]+newWH[1]),
					(position[0][0]+newWH[0], position[0][1]),
					(position[0][0], position[0][1])]
		for newTL in newCoords:
			self.terrain.append(block((newTL, newWH)))
		del self.terrain[index]

	def cleanupTerrain(self):
		for i in range(len(self.terrain)-1, -1, -1):
			if self.terrain[i].removed == True:
				#print "Removing"
				del self.terrain[i]

	def drawTerrain(self, screen):
		for each in self.terrain:
			pygame.gfxdraw.box(screen, each, each.color)

if __name__ == "__main__":

	AIRSPACE = 0
	WIDTH = 512
	HEIGHT = WIDTH + AIRSPACE
	SIZE = (WIDTH,HEIGHT)
	TERRAINSIZE = (WIDTH,WIDTH)
	FPS = 60
	fpsClock = pygame.time.Clock()

	SCREEN = pygame.display.set_mode(SIZE)
	print "Initiated SCREEN"
	pygame.display.set_caption('Destructable Terrain')

	startingblock=((0,AIRSPACE),TERRAINSIZE)
	print startingblock
	mouserect = pygame.Rect((-8,-8),(8,8))

	DT = DestructibleTerrain(startingblock, smallest=1)
	print "DestructibleTerrain Enabled"
	mousepos = None

	while True:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEMOTION:
				mousepos = event.pos
				#print mousepos

			if event.type == pygame.KEYDOWN:
				for i in DT.terrain:
					print i.size

		if mousepos != None:
			mouserect.center = mousepos
			DT.destroyTerrainAt(mouserect)

		SCREEN.fill((0,0,0))
		DT.drawTerrain(SCREEN)

		pygame.display.update()
		fpsClock.tick(FPS)
