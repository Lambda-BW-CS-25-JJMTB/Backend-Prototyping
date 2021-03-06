from Queue import Queue
from Position import Position
from CardinalDirection import CardinalDirection
from Room import Room
# from Player import Player # ready for importing
import random
import time

class RoomController():
    def __init__(self, roomLimit=100):
        self.roomLimit = roomLimit
        self.generateRooms()

    def toDict(self):
        newDict = {}
        roomDict = {}
        for room in self.rooms:
            roomDict[room.id] = room.toDict()
        newDict["rooms"] = roomDict
        newDict["roomCoordinates"] = [pos.toArray() for pos in self.roomCoordinates]
        newDict["spawnRoom"] = self.spawnRoom.id
        return newDict

    def resetAllRooms(self):
        self.rooms = set()
        self.occupiedRooms = set()
        self.emptyRooms = set()
        self.roomCoordinates = set()

        self.spawnRoom = Room("Spawn Area")
        self.addRoomConnection(self.spawnRoom, None, None)

    def generateRooms(self, seed=time.time()):
        self.resetAllRooms()
        random.seed(seed)

        roomQueue = Queue()
        roomQueue.enqueue(self.spawnRoom)

        while len(self.rooms) < self.roomLimit:
            if len(roomQueue) == 0:
                print("Somehow there are no valid rooms in the queue")
                return
            oldRoom = roomQueue.dequeue()
            newRoom = Room(f"Room {len(self.rooms)}")

            possibleDirections = list(self.roomEligibleDirections(oldRoom))
            possibleDirections.sort()
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
        xOffset = 0 - xValues[0]
        yRange = yValues[-1] - yValues[0]
        yOffset = 0 - yValues[0]

        yTemplateArray = [" "] * (yRange + 1)

        xTemplateArray = [yTemplateArray.copy() for i in range(xRange + 1)]

        for room in self.rooms:
            xIndex = xOffset + room.position.x
            yIndex = yOffset + room.position.y
            xTemplateArray[xIndex][yIndex] = "O" if room.position == Position.zero() else room.visualizeTextCharacter()

        outStr = ""
        for yIndex in range(yRange - 1, 0, -1):
            for xIndex in range(xRange):
                outStr += xTemplateArray[xIndex][yIndex]
            outStr += "\n"

        print(outStr)

