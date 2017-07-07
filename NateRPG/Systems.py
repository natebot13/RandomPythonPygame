import pygame
from math import pi, sin, cos, atan2, degrees

class System:
    def SID(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.SID()

    def start(self, entities):
        pass

    def update(self, entity, dt):
        pass

    def end(self):
        pass

class PreSystem:
    def SID(self):
        return self.__class.__name__

class Move(System):
    def __init__(self, scalefactor):
        self.scalefactor = scalefactor

    operating_components = ['Position', 'Velocity']
    def update(self, entity, dt):
        dx = (dt/1000) * self.scalefactor * entity['Velocity'].speed * cos(entity['Velocity'].angle)
        dy = (dt/1000) * self.scalefactor * entity['Velocity'].speed * -sin(entity['Velocity'].angle)
        if 'Collidable' in entity:
            if entity['Collidable'].colliding['right'] and dx < 0:
                dx = 0
            if entity['Collidable'].colliding['left'] and dx > 0:
                dx = 0
            if entity['Collidable'].colliding['down'] and dy < 0:
                dy = 0
            if entity['Collidable'].colliding['up'] and dy > 0:
                dy = 0
        entity['Position'].x += dx
        entity['Position'].y += dy

class Movable(System):

    operating_components = ['Movable','Controllable', 'Velocity']
    def update(self, entity, dt):
        movable = entity['Movable']
        controls = movable.controls
        for event in entity['Controllable'].getKeyDownEvents(controls):
            if event.key == controls[0]:
                movable.addMove(0)
            if event.key == controls[1]:
                movable.addMove(1)
            if event.key == controls[2]:
                movable.addMove(2)
            if event.key == controls[3]:
                movable.addMove(3)
        for event in entity['Controllable'].getKeyUpEvents(entity['Movable'].controls):
            if event.key == controls[0]:
                movable.removeMove(0)
            if event.key == controls[1]:
                movable.removeMove(1)
            if event.key == controls[2]:
                movable.removeMove(2)
            if event.key == controls[3]:
                movable.removeMove(3)
        if not movable.canMove():
            entity['Velocity'].speed = 0
        else:
            entity['Velocity'].speed = entity['Velocity'].spdCONST
            entity['Velocity'].angle = movable.lastMove() * (pi/2)

class Collide(System):
    operating_components = ['Collidable', 'Position', 'Velocity']

    def __init__(self, collidermanager):
        self.collidermanager = collidermanager

    def update(self, entity, dt):
        if entity['Velocity'].speed > 0:
            for side in entity['Collidable'].colliding:
                    entity['Collidable'].colliding[side] = False
            collrect = entity['Collidable'].collisionrect
            x, y = entity['Position'].xy
            xoff, yoff = entity['Collidable'].xyoffset
            collrect.x, collrect.y = x + xoff, y + yoff
            collisions = entity['Collidable'].collisionrect.collidelistall(self.collidermanager.colliders)
            if collisions:
                for each in collisions:
                    r = self.collidermanager.colliders[each]
                    rightanglerange = (atan2(-r.height + 2, r.width), atan2(collrect.height - 2, r.width))
                    topanglerange = (atan2(collrect.height, r.width - 2), atan2(collrect.height, -collrect.width + 2))
                    leftanglerange = (atan2(-r.height + 2, -collrect.width), atan2(collrect.height - 2, -collrect.width))
                    bottomanglerange = (atan2(-r.height, -collrect.width + 2), atan2(-r.height, r.width - 2))
                    angle = atan2((r.y - collrect.y),(collrect.x - r.x))
                    if rightanglerange[0] < angle < rightanglerange[1]:
                        entity['Collidable'].colliding['right'] = True
                    elif topanglerange[0] < angle < topanglerange[1]:
                        entity['Collidable'].colliding['up'] = True
                    elif angle < leftanglerange[0] or angle > leftanglerange[1]:
                        entity['Collidable'].colliding['left'] = True
                    elif bottomanglerange[0] < angle < bottomanglerange[1]:
                        entity['Collidable'].colliding['down'] = True

class Interact(System):
    operating_components = ['Interactor', 'Controllable', 'Collidable']

    def update(self, entity, dt):
        pass

class Render(System):
    def __init__(self, screen):
        self.screen = screen

    operating_components = ['Renderable', 'Position']
    def update(self, entity, dt):
        face = 0
        frame = 0
        width, height = entity['Renderable'].sprite.get_size()
        if 'Multifaced' in entity:
            height = entity['Multifaced'].spriteheight
            face = entity['Multifaced'].face
        if 'Animated' in entity:
            width = entity['Animated'].spritewidth
            frame = entity['Animated'].getFrame(dt)

        sf = entity['Renderable'].scalefactor
        sprite = entity['Renderable'].sprite.subsurface(pygame.Rect((frame * width, face * height),(width, height)))
        self.screen.blit(pygame.transform.scale(sprite, (int(width * sf), int(height * sf))), entity['Position'].xy)

        if 'Collidable' in entity:
            pygame.draw.rect(self.screen, (255,0,0), entity['Collidable'].collisionrect, 3)

class AnimateWhenMoving(System):
    operating_components = ['MovementAnimation', 'Velocity', 'Animated']

    def update(self, entity, dt):
        if entity['Velocity'].speed != 0:
            entity['Animated'].active = True
        else:
            entity['Animated'].active = False

class Multifaced(System):
    operating_components = ['Multifaced', 'Velocity']

    def update(self, entity, dt):
        entity['Multifaced'].face = entity['Velocity'].angle//(pi/2)

class KeyboardInput(System):
    operating_components = ['Controllable']
    events = []

    def start(self, e):
        self.events = pygame.event.get([pygame.KEYDOWN, pygame.KEYUP])

    def update(self, entity, dt):
        for event in self.events:
            if event.key in entity['Controllable'].controls:
                entity['Controllable'].events.append(event)

    def end(self):
        pygame.event.clear()

class SortByY(System):
    operating_components = []

    def __init__(self, entitymanager, maxY):
        self.entitymanager = entitymanager
        self.maxY = maxY

    def start(self, entities):
        for i in range(len(entities) - 1 , 0, -1):
            ent = self.entitymanager.getEntity(entities[i])
            entY = 0
            if 'Collidable' in ent:
                entY = ent['Collidable'].collisionrect.bottom
            elif 'Collider' in ent:
                entY = ent['Collider'].collisionrect.bottom
            elif 'Top' in ent:
                entY = self.maxY
            self.rise(entY, entities, i)

    def rise(self, entY, entities, i):
        if i < len(entities) - 1:
            nextY = 0
            nextAboveAll = False
            nextEnt = self.entitymanager.getEntity(entities[i + 1])
            if 'Collider' in nextEnt:
                nextY = nextEnt['Collider'].collisionrect.bottom
            elif 'Collidable' in nextEnt:
                nextY = nextEnt['Collidable'].collisionrect.bottom
            elif 'Top' in nextEnt:
                nextY = self.maxY
            if entY > nextY:
                entities[i + 1], entities[i] = entities[i], entities[i + 1]
                self.rise(entY, entities, i + 1)