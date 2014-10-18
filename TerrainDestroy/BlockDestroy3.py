import pygame, random, pymunk
from pymunk import Vec2d
import pymunk.util as u

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
	
	def flipyv(self, v):
		return int(v.x), int(-v.y+self.SIZE[1])
		
	def __init__(self):
		pygame.init()
		
		self.SIZE = (512, 512)
		self.SMALLEST = 8
		self.FPS = 30
		self.fpsClock = pygame.time.Clock()
		
		self.SCREEN = pygame.display.set_mode(self.SIZE)
		pygame.display.set_caption('Terrain Test')

		self.terrain = [block(pygame.Rect((0,0),self.SIZE))]
		self.mousepos = None
		
		### Init pymunk and create space
		self.space = pymunk.Space()
		self.space.gravity = (0.0, 100.0)
		
		self.polys = []
		
	def create_box(self, pos, size = "default", mass = 1.0):
		if size == "default":
			size = self.SMALLEST/2
		else:
			size = size/2
		box_points = map(Vec2d, [(-size, -size), (-size, size), (size,size), (size, -size)])
		return self.create_poly(box_points, mass = mass, pos = pos)
		
	def create_poly(self, points, mass = 5.0, pos = (0,0)):
		moment = pymunk.moment_for_poly(mass,points, Vec2d(0,0))	
		#moment = 1000
		body = pymunk.Body(mass, moment)
		body.position = Vec2d(pos)	   
		print body.position
		shape = pymunk.Poly(body, points, Vec2d(0,0))
		shape.friction = 0.5
		shape.collision_type = 0
		self.space.add(body, shape)
		return shape
	
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
		for i in splitthese:	
			position = (self.terrain[i].rect.topleft, self.terrain[i].rect.size)
			del self.terrain[i]
			newWH = (position[1][0]/2, position[1][1]/2)
			newCoords = [(position[0][0], position[0][1]),
						(position[0][0]+newWH[0], position[0][1]),
						(position[0][0], position[0][1]+newWH[1]),
						(position[0][0]+newWH[0], position[0][1]+newWH[1])]
			for j in range(3,-1,-1):
				self.terrain.insert(i, block(pygame.Rect(newCoords[j],newWH)))
				#print self.terrain
	
	def removePeice(self, point):
		removelist = []
		for i in range(0, len(self.terrain)):
			if self.terrain[i].rect.collidepoint(point):
				removelist.append(i)
		for i in removelist:
			self.polys.append(self.create_box(pos=self.terrain[i].rect.center))
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
				
	def draw_poly(self, poly):
		body = poly.body
		ps = poly.get_vertices()
		ps.append(ps[0])
		#ps = map(self.flipyv, ps)
		#if u.is_clockwise(ps):
		#	color = THECOLORS["green"]
		#else:
		#	color = THECOLORS["red"]
		color = randomColor()
		pygame.draw.lines(self.SCREEN, color, False, ps)
	
	def updateScreen(self):
		self.SCREEN.fill((0,0,0))
		for i in range(0, len(self.terrain)):
			pygame.draw.rect(self.SCREEN, self.terrain[i].color, self.terrain[i])
		for poly in self.polys:
			self.draw_poly(poly)
		self.space.step(1.0/float(self.FPS))
		pygame.display.update()
		self.fpsClock.tick(self.FPS)
		
	def removeFarPieces(self):
		xs = []
		for poly in self.polys:
			if poly.body.position.x < -1000 or poly.body.position.x > 1000 \
				or poly.body.position.y < -1000 or poly.body.position.y > 1000:
				xs.append(poly)
		
		for poly in xs:
			self.space.remove(poly, poly.body)
			self.polys.remove(poly)

if __name__ == "__main__":
	bd = blockDestroy()
	while True:
		mousepos = bd.getClickedPoint()
		if mousepos != None:
			bd.destroyPeice(mousepos)
		bd.updateScreen()
		bd.removeFarPieces()
