import math
#creating vector
#vector is being used to keep track of position and velocity
class Vectors(object):
    #basic vector stuff needed
    def __init__(self, x=0, y=0):
        #x and y are variables to creat the coordinates for the vector to point towards
        self.x = x 
        self.y = y
        #thresh is needed to make the calculations for coordinates and such
        #allows me to say that a slight difference is actually the same number
        self.thresh = 0.000001
    #actual calculations for coordinates
    def __add__(self, other):
        return Vectors(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vectors(self.x - other.x, self.y - other.y)
    def __neg__(self):
        return Vectors(-self.x, -self.y)
    #scalar has to do with speed (look it up loser)
    def __mul__(self, scalar):
        return Vectors(self.x * scalar, self.y * scalar)
    def __div__(self, scalar):
        if scalar != 0:
            return Vectors(self.x / float(scalar), self.y / float(scalar))
        return None
    #checks for equality between vectors
    #this is where thress is needed to make it a little less specific
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False
    #using magnitude method would require square roots
    #instead using the magnitude squared method i can avoid this making it slightly easier to compare the length of two vectors
    #this is where the math module is needed
    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())
    #the copy method allows me to copy a vector so i can get a new instance of it
    #with how python stores variables in memory, it lets me modify the new object without touching the old one
    def copy(self):
        return Vectors(self.x, self.y)
    def asTuple(self):
        return self.x, self.y
    def asInt(self):
        return int(self.x), int(self.y)
    #this part isnt needed but will make it more convenient to print out the vector easy
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"
