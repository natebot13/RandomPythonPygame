import pygame, sys, math
pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
spacing = ((2.0*math.pi)/len(alphabet))
radius = 230.0
adjustedradius = 230.0
offset = -6.5
mouseloc = (0,0)
runeCharacters = []
runeBoundaries = []
selectedRunes = []
mouseDown = False
hover = [0,False]
spell = []

SCREEN = pygame.display.set_mode((512, 512))
pygame.display.set_caption('Rune Connector')
runes = pygame.font.Font("halfelvenbold.ttf", 32)
glow = pygame.image.load("glow.png").convert_alpha()

for i in range(0, len(alphabet)):
	runeCharacters.append(runes.render(alphabet[i], True, (200,200,255)))
	runeBoundaries.append(runeCharacters[i].get_rect())

while True:
	
	SCREEN.fill((0,0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEMOTION:
			mouseloc = event.pos
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True
		if event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False

	if mouseDown == True:
		for i in range(0, len(runeBoundaries)):
			runeBoundaries[i].center = ((math.cos(i*spacing+offset*spacing)*radius)+256, (math.sin(i*spacing+offset*spacing)*radius)+256)
			if runeBoundaries[i].collidepoint(mouseloc):
				hover = [i, True]
				SCREEN.blit(glow, tuple(x-16 for x in runeBoundaries[i].center))
			SCREEN.blit(runeCharacters[i], runeBoundaries[i])
			
		if hover[1] and not runeBoundaries[hover[0]].collidepoint(mouseloc):
			hover[1] = False
			selectedRunes.append(hover[0])
			
		if len(selectedRunes) > 0:
			linelist = [mouseloc]
			for rune in selectedRunes:
				linelist.insert(-1, runeBoundaries[rune].center)
			pygame.draw.lines(SCREEN, (200,200,255), False, linelist, 3)
		offset+=.004
	else:
		offset+=.05
		hover = (0, False)
		if len(selectedRunes) > 0:
			adjustedradius-=2
			for rune in selectedRunes:
				runeBoundaries[rune].center = ((math.cos(rune*spacing+offset*spacing)*adjustedradius)+256, (math.sin(rune*spacing+offset*spacing)*adjustedradius)+256)
				SCREEN.blit(runeCharacters[rune], runeBoundaries[rune])
		if adjustedradius < 0:
			spell = []
			print selectedRunes
			for rune in selectedRunes:
				spell.append(alphabet[rune])
			adjustedradius = radius
			selectedRunes = []
	print selectedRunes
	word = runes.render(''.join(spell), True, (200,200,255))
	wordCenter = word.get_rect()
	wordCenter.center = (256,256)
	SCREEN.blit(word, wordCenter)
					
	pygame.display.update()
	fpsClock.tick(FPS)

