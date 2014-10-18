import pygame, sys, time, random, math

class Orb():
	def __init__(self, (x, y), radius, color = None):
		print "Orb created"
		self.x = x
		self.y = y
		self.center = (x, y)
		self.radius = radius
		if color == None:
			self.color = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
			print self.color
		else:
			self.color = color
		assert len(self.color) == 3
		

def main():
	
	pygame.mixer.init()
	
	WIDTH = 512
	HEIGHT = 512
	SIZE = (WIDTH,HEIGHT)
	FPS = 60
	SCREEN = pygame.display.set_mode(SIZE)
	pygame.display.set_caption("Dolphin Tank")
	CLOCK = pygame.time.Clock()
	mousepos = (0,0)
	mouseOrb = Orb((0,0), 64, (10,200,255))
	numOrbiters = 5
	orbiters = []
	orbiterRadius = 100
	orbiterSpacing = math.pi*2/numOrbiters
	orbiterSpeed = .03
	for i in range(numOrbiters):
		orbiters.append(Orb((0,0), 2, mouseOrb.color))
	clicked = False
	extra = 0.0
	pygame.mixer.music.load("01-01- In the Dolphin Tank.mp3")
	pygame.mixer.music.play()
	
	while True:
		
		SCREEN.fill((0,0,0))
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				#~ print "Clicked!"
				clicked = True
			if event.type == pygame.MOUSEBUTTONUP:
				#~ print "Unclicked!"
				clicked = False
			if event.type == pygame.MOUSEMOTION:
				mousepos = event.pos
		if clicked == True:
			#~ print "Drawing!"
			 
			pygame.draw.circle(SCREEN, mouseOrb.color, mousepos, mouseOrb.radius)
			extra+=orbiterSpeed
			if extra > 2*math.pi:
				extra = 0
			orbiterRadius+=math.sin(extra)
			print orbiterRadius
			for i in range(len(orbiters)):
				pygame.draw.circle(SCREEN, orbiters[i].color, (int(orbiterRadius*(math.cos((orbiterSpacing*i)+extra)))+mousepos[0],int(orbiterRadius*(math.sin((orbiterSpacing*i)+extra)))+mousepos[1]), orbiters[i].radius)
			
		pygame.display.update()
		CLOCK.tick(FPS)


if __name__ == "__main__":
	main()
