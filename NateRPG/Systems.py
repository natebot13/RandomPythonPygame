import pygame
from math import pi, sin, cos, atan2, degrees

class System:
    def SID(self):
        return self.__class__.__name__

class Move(System):
    operating_components = ['Position', 'Velocity']
    def update(self, entity, dt):
        # print('Input xDir:', entity['Input'].xDir)
        entity['Position'].x += entity['Velocity'].speed*cos(entity['Velocity'].angle)
        entity['Position'].y += entity['Velocity'].speed*sin(entity['Velocity'].angle)

class KeyboardInput(System):
    operating_components = ['Controllable']
    up, down = 0, 0
    left, right = 0, 0

    def update(self, entity, dt):
        repost = []
        for event in pygame.event.get():
            print(event)
            # print(entity['Controllable'].controls)
            # if event.type in entity['Controllable'].controls:
            #     print("handing event over")
            #     entity['Controllable'].events.append(event)
        # for e in repost:
        #     pygame.event.post(e)




            # == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         self.up = -1
            #     if event.key == pygame.K_DOWN:
            #         self.down = 1
            #     if event.key == pygame.K_LEFT:
            #         self.left = -1
            #     if event.key == pygame.K_RIGHT:
            #         self.right = 1
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_UP:
            #         self.up = 0
            #     if event.key == pygame.K_DOWN:
            #         self.down = 0
            #     if event.key == pygame.K_LEFT:
            #         self.left = 0
            #     if event.key == pygame.K_RIGHT:
            #         self.right = 0
            # x = self.left + self.right
            # y = self.up + self.down
            # if x == 0 and y == 0:
            #     entity['Velocity'].speed = 0
            # else:
            #     entity['Velocity'].speed = entity['Velocity'].spdCONST
            #     entity['Velocity'].angle = atan2(y, x)

class Render(System):
    def __init__(self, screen):
        self.screen = screen

    operating_components = ['Renderable', 'Position', 'Velocity']
    def update(self, entity, dt):
        row = entity['Velocity'].angle//(pi/2)
        self.screen.blit(entity['Renderable'].getFrame(row, dt), entity['Position'].xy)

class SystemsManager:
    def __init__(self, entity_manager, screen):
        self.entity_manager = entity_manager
        # BE SURE TO ADD ALL SYSTEMS TO THIS SYSTEM INIT LIST #
        self.registeredSystems = [KeyboardInput(), Move(), Render(screen)]
        # END SYS INIT LIST #

#### DO NOT EDIT BELOW THIS ####

    def runSystems(self, dt):
        for entitynum in self.entity_manager.allEntities():
            print("Operating on entity: ", entitynum)
            for system in self.registeredSystems:
                if self.entity_manager.entityHasComponents(entitynum, system.operating_components):
                    print("Running system: ", system.SID())
                    system.update(self.entity_manager.getEntity(entitynum), dt)

    def endStep(self):
        pygame.event.clear()

    def registerSystem(self, system):
        self.registeredSystems.append(system())

    def allSystems(self):
        for system in registeredSystems:
            yield system