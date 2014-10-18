import numpy, pygame, random, pyganim, os

class SuperBean():
	def __init__(self, (x,y)):
		self.Bean = pygame.image.load("images/SuperBean.png").convert_alpha()
		imagesAndDurations = [('images/cape/frame_%s.gif' % (str(num).rjust(3, '0')), 0.1) for num in range(len(os.listdir("images")))]
		self.Cape = pyganim.PygAnimation(imagesAndDurations)
		self.CapeConductor = pyganim.PygConductor(self.Cape)
		self.CapeConductor.play()
		self.x = x
		self.y = y
		self.center = (x,y)
		self.BeanRect = self.Bean.get_rect()
		self.BeanRect.center = self.center
		
	def draw(self, screen):
		self.x, self.y = self.center
		self.BeanRect.center = self.center
		self.Cape.blit(screen, (self.x-150,self.y-70))
		screen.blit(self.Bean, self.BeanRect)

def main():
	SIZE = (512,512)
	WIDTH = SIZE[0]
	HEIGHT = SIZE[1]
	SCREEN = pygame.display.set_mode(SIZE)
	pygame.display.set_caption("Super Bean")
	pygame.mouse.set_visible(False)
	
	mousepos = (0,0)
	SB = SuperBean(mousepos)
	
	while True:
		
		for event in pygame.event.get():
			if event.type == pygame.MOUSEMOTION:
				mousepos = event.pos
		
		SB.center = mousepos

		SCREEN.fill((10, 200, 255))
		SB.draw(SCREEN)
		pygame.display.update()

if __name__ == "__main__":
	main()
