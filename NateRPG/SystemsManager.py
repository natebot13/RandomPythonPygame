from Systems import *

class SystemsManager:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.registeredSystems = []

    def registerSystem(self, system):
        self.registeredSystems.append(system)

    def runSystems(self, dt):
        entities = self.entity_manager.allEntities()
        for system in self.registeredSystems:
            system.start(entities)
            for entitynum in entities:
                if self.entity_manager.entityHasComponents(entitynum, system.operating_components):
                    system.update(self.entity_manager.getEntity(entitynum), dt)
            system.end()

    def endStep(self):
        pygame.display.update()

    def allSystems(self):
        for system in registeredSystems:
            yield system