class System:
    def SID(self):
        return self.__class__.__name__

class Move(System):
    operating_components = ['Movable']
    def update(self, entityComponents):
        print(entityComponents['Movable'].x)
        print(entityComponents['Movable'].y)
        entityComponents['Movable'].x += entityComponents['Movable'].xvel
        entityComponents['Movable'].y += entityComponents['Movable'].yvel

#### DO NOT EDIT BELOW THIS ####

class SystemsManager:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        # BE SURE TO ADD ALL SYSTEMS TO THIS SYSTEM INIT LIST #
        self.registeredSystems = [Move()]
        # END SYS INIT LIST #

    def runSystems(self):
        for entity in self.entity_manager.allEntities():
            for system in self.registeredSystems:
                if self.entity_manager.entityHasComponents(entity, system.operating_components):
                    system.update(self.entity_manager.getEntity(entity))

    def registerSystem(self, system):
        self.registeredSystems.append(system())

    def allSystems(self):
        for system in registeredSystems:
            yield system