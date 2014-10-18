from Systems import *
from EntityManager import *
from Components import *

entManager = EntityManager()
sysManager = SystemsManager(entManager)
ID = entManager.newEntity()
entManager.addComponentToEntity(ID, Movable(xvel=2))
ID = entManager.newEntity()
entManager.addComponentToEntity(ID, Movable(yvel=5))
while True:
    sysManager.runSystems()