import pygame
import os, sys
import MapManager, EntityManager, SystemsManager, ColliderManager, Components, Systems

def main():    
    pygame.mixer.init()
    
    NUMTILES = (16, 16)
    TILESIZE = (16, 16)
    SMALLSIZE = (NUMTILES[0] * TILESIZE[0], NUMTILES[1] * TILESIZE[1])
    SCALEFACTOR = 3
    ENTITYSCALEFACTOR = 1.75
    WIDTH = SMALLSIZE[0] * SCALEFACTOR
    HEIGHT = SMALLSIZE[1] * SCALEFACTOR
    SIZE = (WIDTH,HEIGHT)
    FPS = 60
    CLOCK = pygame.time.Clock()

    icon = pygame.image.load('textures/blue_n.png')
    icon.set_colorkey((0,255,0))
    pygame.display.set_icon(icon)
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Nate's RPG")

    entManager = EntityManager.EntityManager()
    sysManager = SystemsManager.SystemsManager(entManager)
    collManager = ColliderManager.ColliderManager(SCALEFACTOR, ENTITYSCALEFACTOR)

    m = MapManager.MapManager("blowharderterrain.png", "blowharderterrain.col", TILESIZE)
    room = m.loadRoom("titlescreen", entManager, collManager)
    smallscreen = pygame.Surface(SMALLSIZE)

    sysManager.registerSystem(Systems.KeyboardInput())
    sysManager.registerSystem(Systems.Movable())
    sysManager.registerSystem(Systems.AnimateWhenMoving())
    sysManager.registerSystem(Systems.Multifaced())
    sysManager.registerSystem(Systems.Move(ENTITYSCALEFACTOR))
    sysManager.registerSystem(Systems.Collide(collManager))
    sysManager.registerSystem(Systems.SortByY(entManager, HEIGHT))
    sysManager.registerSystem(Systems.Render(SCREEN))

    ID = entManager.newEntity()
    entManager.addComponentToEntity(ID, Components.Position(WIDTH/2, HEIGHT/2))
    entManager.addComponentToEntity(ID, Components.Velocity())
    entManager.addComponentToEntity(ID, Components.Collidable(pygame.Rect(4,8,9,8), ENTITYSCALEFACTOR))
    entManager.addComponentToEntity(ID, Components.Renderable(ENTITYSCALEFACTOR, 'boy/boy_green.png'))
    entManager.addComponentToEntity(ID, Components.Animated())
    entManager.addComponentToEntity(ID, Components.Multifaced())
    entManager.addComponentToEntity(ID, Components.MovementAnimation())
    entManager.addComponentToEntity(ID, Components.Movable([pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s]))
    entManager.addComponentToEntity(ID, Components.Controllable([pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_SPACE]))

    while True:
        
        SCREEN.fill((0, 0, 0))
        room.draw(smallscreen)
        pygame.transform.scale(smallscreen, SCREEN.get_rect().size, SCREEN)
        sysManager.runSystems(CLOCK.get_time())
        for each in collManager.colliders:
            pygame.draw.rect(SCREEN, (255,0,0), each, 3)
        sysManager.endStep()
        CLOCK.tick(FPS)
        # print(CLOCK.get_fps())

if __name__ == "__main__":
    # import cProfile as profile
    # profile.run('main()')
    main()