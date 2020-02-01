import unittest
from Room import Room, Position, Player, Rooms


class RoomTests(unittest.TestCase):
    def setUp(self):
        pass

    def testPosition(self):
        position = Position(23.547, 29.557)
        self.assertEqual(position.x, 23.547)
        self.assertEqual(position.y, 29.557)

        zPos = Position.zero()
        self.assertEqual(zPos.x, 0)
        self.assertEqual(zPos.y, 0)

        distance = zPos.distanceTo(position)
        37.78991
        self.assertEqual(distance, 37.78991211950618)

        gtTest = zPos.distanceIsGreaterThan(position, 35)
        self.assertEqual(gtTest, True)
        gtTest = zPos.distanceIsGreaterThan(position, 40)
        self.assertEqual(gtTest, False)

        otherPos = Position(0, 0)

        self.assertEqual(position == otherPos, False)
        self.assertEqual(position != otherPos, True)
        self.assertEqual(otherPos == zPos, True)
        self.assertEqual(otherPos != zPos, False)

if __name__ == '__main__':
    unittest.main()
