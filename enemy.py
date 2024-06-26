import pygame
from pygame.locals import *
from vector import Vectors
from constants import *
from random import randint

#General properties and such of all entities, fruit, pacman, ghosts, pellets
class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vectors(0, -1), DOWN:Vectors(0, 1),
                           LEFT:Vectors(-1, 0), RIGHT:Vectors(1,0), STOP:Vectors()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None

#sets the node position of the entity
    def setPosition(self):
        self.position = self.node.position.copy()

#updates the positin of th entity
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt

        if self.overshotTarget():
            self.node = self.target
            directions =  self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

#checks to see if direction is valid
    def validDirection(self, direction):
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

#gets a new target direction
    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

#for actually moving to the node
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False
    
#stops ghost from moving in the direction it came
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

#allows the ghost to go in the direction from where it came
    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

#defines what the directions are
    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

#for choosing a random directions
    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]

#sets a goal direction
    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]

#needed to set the starting node for entities
    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

#for setting entities between nodes
    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position)
            self.position = Vectors.__div__(self.position,2)
#for reseting entity info
    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

#this is so that if the maze is bigger the speed can be adjusted, that way everything doesnt look like it's moving slower
    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

#for rendering entities
    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vectors(TILEWIDTH, TILEHEIGHT)
                adjust = Vectors.__div__(adjust, 2)
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)
