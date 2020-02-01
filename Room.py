from enum import Enum
from Queue import Queue
import math
import random

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


class CardinalDirection(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

class RoomController():
    def __init__(self, roomLimit=100):
        self.roomLimit = roomLimit
        self.generateRooms()

    def generateRooms(self, seed=None):
        self.rooms = set()
        self.occupiedRooms = set()
        self.emptyRooms = set()
        self.roomCoordinates = set()
        random.seed(seed)

        self.spawnRoom = Room("Spawn Area")
        self.addRoomConnection(self.spawnRoom, None, None)

        roomQueue = Queue()
        roomQueue.enqueue(self.spawnRoom)

        while len(self.rooms) < self.roomLimit:
            if len(roomQueue) == 0:
                print("Somehow there are no valid rooms in the queue")
                return
            oldRoom = roomQueue.dequeue()
            newRoom = Room(f"Room {len(self.rooms)}")

            possibleDirections = list(self.roomEligibleDirections(oldRoom))
            if len(possibleDirections) > 0:
                newDirection = random.choice(possibleDirections)
                self.addRoomConnection(newRoom, oldRoom, newDirection)
                if self.roomEligibleToAppend(newRoom):
                    roomQueue.enqueue(newRoom)
                if self.roomEligibleToAppend(oldRoom):
                    roomQueue.enqueue(oldRoom)

    # must include an oldRoom and direction or the new room will sit abandoned and alone. Exception is made for initial room.
    def addRoomConnection(self, newRoom, oldRoom, direction):
        if oldRoom and direction:
            if direction == CardinalDirection.NORTH:
                oldRoom.connectNorthTo(newRoom)
            elif direction == CardinalDirection.EAST:
                oldRoom.connectEastTo(newRoom)
            elif direction == CardinalDirection.SOUTH:
                oldRoom.connectSouthTo(newRoom)
            elif direction == CardinalDirection.WEST:
                oldRoom.connectWestTo(newRoom)
            else:
                # something went wrong
                return
        self.rooms.add(newRoom)
        self.emptyRooms.add(newRoom)
        self.roomCoordinates.add(newRoom.position)

    # checks to see how many NSEW neighbors a new room would potentially have. returns true if the neighbor count is 1
    def canAddRoomAt(self, position):
        nswe = [pos for pos in (position.nsewOne())]

        count = len([direction for direction in nswe if direction in self.roomCoordinates])
        if count == 1:
            return True
        else:
            return False

    def roomEligibleDirections(self, room):
        n, s, e, w = room.position.nsewOne()
        eligibleDirections = set()
        if self.canAddRoomAt(n):
            eligibleDirections.add(CardinalDirection.NORTH)
        if self.canAddRoomAt(s):
            eligibleDirections.add(CardinalDirection.SOUTH)
        if self.canAddRoomAt(e):
            eligibleDirections.add(CardinalDirection.EAST)
        if self.canAddRoomAt(w):
            eligibleDirections.add(CardinalDirection.WEST)
        return eligibleDirections

    def roomEligibleToAppend(self, room):
        return len(self.roomEligibleDirections(room)) > 0

    def textVisualization(self):
        xValueSet = {room.position.x for room in self.rooms}
        yValueSet = {room.position.y for room in self.rooms}
        xValues = sorted(list(xValueSet))
        yValues = sorted(list(yValueSet))

        xRange = xValues[-1] - xValues[0]
        yRange = yValues[-1] - yValues[0]

        yTemplateArray = [" "] * yRange * 2
        # xTemplateArray = [yTemplateArray.copy()].copy() * xRange * 2

        xTemplateArray = [yTemplateArray.copy() for i in range(xRange * 2)]

        for room in self.rooms:
            xIndex = xRange + room.position.x
            yIndex = yRange + room.position.y
            xTemplateArray[xIndex][yIndex] = "o" if room.position == Position.zero() else "x"

        # print("x: ", xValues, xRange)
        # print("y: ", yValues, yRange)


        outStr = ""
        for yIndex in range(yRange * 2):
            for xIndex in range(xRange * 2):
                outStr += xTemplateArray[xIndex][yIndex]
            outStr += "\n"

        print(outStr)


roomController = RoomController()
roomController.textVisualization()
