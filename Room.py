from Queue import Queue
import math

class Position():
    @staticmethod
    def zero():
        return Position(0, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Position(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return Position(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        return Position(self.x // other.x, self.y // other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def nsewOne(self):
        northOne = self + Position(0, 1)
        southOne = self + Position(0, -1)
        westOne = self + Position(-1, 0)
        eastOne = self + Position(1, 0)
        return (northOne, southOne, eastOne, westOne)

    def __distanceToNoRoot(self, toPosition):
        return (self.x - toPosition.x) * (self.x - toPosition.x) + (self.y - toPosition.y) * (self.y - toPosition.y)

    def distanceTo(self, toPosition):
        return math.sqrt(self.__distanceToNoRoot(toPosition))

    def distanceIsGreaterThan(self, toPosition, comparedValue):
        return self.__distanceToNoRoot(toPosition) > (comparedValue * comparedValue)

    def __repr__(self):
        return f"({repr(self.x)}, {repr(self.y)})"

    def __str__(self):
        return f"({str(self.x)}, {str(self.y)})"

    def __hash__(self):
        return hash(repr(self))

class Player():
    def __init__(self):
        self.room = None
        self.position = Position.zero()

class Room():
    def __init__(self, name, position=Position.zero(), north=None, south=None, east=None, west=None):
        self.name = name
        self.position = position
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.players = set()
        self.itemReward = None

    def connectNorthTo(self, room):
        self.north = room
        relativePosition = Position(0, 1)
        self.north.position = self.position + relativePosition
        if room.south != self:
            room.connectSouthTo(self)

    def connectSouthTo(self, room):
        self.south = room
        relativePosition = Position(0, -1)
        self.south.position = self.position + relativePosition
        if room.north != self:
            room.connectNorthTo(self)

    def connectEastTo(self, room):
        self.east = room
        relativePosition = Position(1, 0)
        self.east.position = self.position + relativePosition
        if room.west != self:
            room.connectWestTo(self)

    def connectWestTo(self, room):
        self.west = room
        relativePosition = Position(-1, 0)
        self.west.position = self.position + relativePosition
        if room.east != self:
            room.connectEastTo(self)

    def __str__(self):
        connectedRooms = [self.north, self.south, self.east, self.west]
        connectionCount = len(connectedRooms)
        roomsString = "room" + ("" if connectionCount == 1 else "s")
        return f"Room: {self.name} - connected to {connectionCount} {roomsString}"


class Rooms():
    def __init__(self, roomLimit=100):
        self.roomLimit = roomLimit
        self.generateRooms()

    def generateRooms(self):
        self.rooms = set()
        self.occupiedRooms = set()
        self.emptyRooms = set()

        entrance = Room("Spawn Area")
        self.addRoom(entrance)

    def addRoom(self, room):
        self.rooms.add(room)
        self.emptyRooms.add(room)


room = Room("entrance", Position(1, 5))

print(room)
