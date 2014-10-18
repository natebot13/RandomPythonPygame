import pygame, sys, math
pygame.init()

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
spacing = ((2.0*math.pi)/len(alphabet))
radius = 230.0
offset = .75
letterblocks = []
letterblocksrects = []
mousetoggle = 0
selectedrunes = []
mouseloc = (0,0)
decay = 0.0

SCREEN = pygame.display.set_mode((512, 512))
runes = pygame.font.Font("halfelvenbold.ttf", 32)
glow = pygame.image.load("glow.png").convert_alpha()
	
while True:
	SCREEN.fill((255,255,255))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEMOTION:
			mouseloc = event.pos
		if event.type == pygame.MOUSEBUTTONDOWN:
			mousetoggle = 1
			i = 0
			for letter in alphabet:
				letterblocks.append(runes.render(letter, True, (150,150,255)))
				letterblocksrects.append(letterblocks[i].get_rect())
				i+=1
		if event.type == pygame.MOUSEBUTTONUP:
			linelist.pop()
			mousetoggle = 0
			decay = 100.0
			
			
	if len(selectedrunes) > 2:
		for rune in selectedrunes:
			SCREEN.blit(letterblocks[rune], letterblocksrects[rune])
	if decay <= 0:
		selectedrunes = []
		offset = .75
		radius = 230.0
		decay = 0
	print event.type
	if mousetoggle == 1:
		i = 0
		for block in letterblocks:
			letterblocksrects[i].center = ((((math.cos(float(i+(len(alphabet)*offset))*float(spacing)))*radius)+256), (((math.sin(float(i+(len(alphabet)*offset))*float(spacing)))*radius)+256))
			if letterblocksrects[i].collidepoint(mouseloc):
				SCREEN.blit(glow, tuple(x-16 for x in letterblocksrects[i].center))
				selectedrunes.append(i)
			SCREEN.blit(block, letterblocksrects[i])
			i+=1
		offset+=.0002
		#radius-=.1
	linelist = [mouseloc]
	for rune in selectedrunes:
		linelist.insert(-1, letterblocksrects[rune].center)
	if len(linelist) > 1:
		pygame.draw.lines(SCREEN, (130,130,255), False, linelist, 3)
	pygame.display.update()
