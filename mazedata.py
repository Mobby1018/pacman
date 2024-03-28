
from constants import *

#General maze info
class MazeBase(object):
    def __init__(self):
        self.portalPairs = {}
        self.homeoffset = (0, 0)
        self.ghostNodeDeny = {UP:(), DOWN:(), LEFT:(), RIGHT:()}

#for setting the portal pairs
    def setPortalPairs(self,nodes):
        for pair in list(self.portalPairs.values()):
            nodes.setPortalPair(*pair)

#connecting the nodes for the home area
    def connectHomeNodes(self, nodes):
        key = nodes.createHomeNodes(*self.homeoffset)
        nodes.connectHomeNodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connectHomeNodes(key, self.homenodeconnectRight, RIGHT)

#needed to make an offset, the home area is not perfectly lined up on nodes
    def addOffset(self, x, y):
        return x+self.homeoffset[0], y+self.homeoffset[1]

#needed to deny ghost access to get into the home
    def denyGhostsAccess(self, ghosts, nodes):
        nodes.denyAccessList(*(self.addOffset(2, 3) + (LEFT, ghosts)))
        nodes.denyAccessList(*(self.addOffset(2, 3) + (RIGHT, ghosts)))
        for direction in list(self.ghostNodeDeny.keys()):
            for values in self.ghostNodeDeny[direction]:
                nodes.denyAccessList(*(values + (direction, ghosts)))

#maze 1 info
class Maze1(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze1"
        self.portalPairs = {0:((0, 17), (27, 17))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (12, 14)
        self.homenodeconnectRight = (15, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (9, 20)
        self.ghostNodeDeny = {UP:((21, 14), (15, 14), (12, 26), (15, 26)), LEFT:(self.addOffset(2, 3),),
                              RIGHT:(self.addOffset(2, 3),)}

#maze 2 info
class Maze2(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze2"
        self.portalPairs = {0:((0, 4), (27, 4)), 1:((0, 26), (27, 26))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (16, 26)
        self.fruitStart = (11, 20)
        self.ghostNodeDeny = {UP:((9, 14), (18, 14), (11, 23), (16, 23)), LEFT:(self.addOffset(2, 3),),
                              RIGHT:(self.addOffset(2, 3),)}

#grouping mazes
class MazeData(object):
    def __init__(self):
        self.obj = None
        self.mazedict = {0:Maze1, 1:Maze2}

#loads what maze we need
    def loadMaze(self, level):
        self.obj = self.mazedict[level%len(self.mazedict)]()
