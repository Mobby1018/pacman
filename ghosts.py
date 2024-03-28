import pygame
from pygame.locals import *
from vector import Vectors
from constants import *
from enemy import Entity
from modes import ModeController
from sprites import GhostSprites

#Ghost ai basically
class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vectors()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

#updates the ghost stuff
    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

#scatter = ghosts scatter to their set areas
    def scatter(self):
        self.goal = Vectors()

#starts freight mode 
    def startFreight(self):
        FM_sound = pygame.mixer.Sound('Breathing.wav')
        FM_sound.play()
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

#sets the goal to spawn
    def spawn(self):
        self.goal = self.spawnNode.position

#sets the spawn node
    def setSpawnNode(self, node):
        self.spawnNode = node

#starts the spawn mode
    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()
#for returning ghosts to their normal behaviors
    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)

#chase is for setting the goal to pacmans position
    def chase(self):
        self.goal = self.pacman.position

#resets info like points
    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

#info for blinky (red one)
#blinky is pretty much just the code above, blinky tries to take the shortest route to pacman
class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)

#info for Pinky (pink one)
#similar to Blinky but instead of the goal being pacman, the goal is in front of pacman
class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)
    def scatter(self):
        self.goal = Vectors(TILEWIDTH*NCOLS, 0)
    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

#info for Inky (teal one)
#Inky bases his position on both Pacman and Blinky
class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vectors(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2

#info for Clyde (orange one)
#When Clyde is at least 8 tiles away he will chase pacman. Otherwise he will be set in scatter mode.
class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vectors(0, TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

#For grouping the ghosts into one set group
#makes them easier to handle
class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        self.name = ("ghostGroup")
    def __iter__(self):
        return iter(self.ghosts)
    def update(self,dt):
        for ghost in self:
            ghost.update(dt)
    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()
    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2
    def resetPoints(self):
        for ghost in self:
            ghost.points = 200
    def reset(self):
        for ghost in self:
            ghost.reset()
    def hide(self):
        for ghost in self:
            ghost.visible = False
    def show(self):
        for ghost in self:
            ghost.visible = True
    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

