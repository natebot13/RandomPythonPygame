class ColliderManager:
    def __init__(self, scalefactor, entityscalefactor):
        self.colliders = []
        self.scalefactor = scalefactor
        self.entityscalefactor = entityscalefactor

    def newCollider(self, x, y, width, height):
        self.colliders.append(pygame.Rect(x, y, width, height))

    def insertCollider(self, rect, prescale = True):
        if prescale:
            rect.x *= self.scalefactor
            rect.y *= self.scalefactor
            rect.width *= self.scalefactor
            rect.height *= self.scalefactor
        self.colliders.append(rect)
        
    def clearColliders(self):
        self.colliders = []