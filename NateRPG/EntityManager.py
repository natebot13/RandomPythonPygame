class EntityManager:
    def __init__(self):
        self.entityMap = {}
        self.entities = []
        self.usableID = 0
        self.reusableID = []
        
    def newID(self):
        """Creates or reuses an available ID for an entity"""
        if self.reusableID:
            return self.reusableID.pop(), False
        else:
            self.usableID += 1
            return self.usableID - 1, True
        
    def newEntity(self):
        """Returns the unique ID of a newly created entity"""
        ID, new = self.newID()
        if new:
            self.entities.append(ID)
            self.entityMap[ID] = {}
        return ID
    
    def getEntity(self, ID):
        return self.entityMap[ID]

    def deleteEntity(self, ID):
        """Deletes the given entity with this ID"""
        self.entityMap[ID] = {}
        self.reusableID.append(ID)
    
    def addComponentToEntity(self, ID, component):
        """Adds a component to an entity.
        Each entity has a dictionary of its components"""
        self.entityMap[ID][component.CID()] = component
    
    def getEntityComponents(self, ID):
        """Returns a dictionary of the components of the entity"""
        return self.entityMap[ID]
    
    def allEntities(self):
        """Returns a generator (kinda like a list) that yeilds each entity ID in the master dict"""
        return self.entities

    def entityFilter(self, components):
        return [self.entityMap[e] for e in self.entityMap if self.entityHasComponents(e, components)]

    def entityHasComponents(self, ID, components):
        """Checks if the entity has all the components given as a list of strings"""
        componentsInEntity = [ent for ent in self.getEntityComponents(ID).keys() if ent in components]
        return sorted(componentsInEntity) == sorted(components)