"""
Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.

1.
Figure out where the navigation instructions lead. What is the Manhattan distance between that location
and the ship's starting position?

2.
Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.

"""
from collections import OrderedDict
import numpy as np

filename = 'data/input_12.txt'


class Ship:
    direction_conversion = OrderedDict({
        "N": np.array([0, 1]),
        "E": np.array([1, 0]),
        "S": np.array([0, -1]),
        "W": np.array([-1, 0])
    })

    def __init__(self, location, facing):
        self.location = location
        self.facing = facing

    def move(self, instruction):
        code = instruction[0]
        number = int(instruction[1:])
        assert number >= 0, "Number in instruction must be positive!"
        if code in self.direction_conversion.keys():
            self.location += self.direction_conversion[code] * number
        elif code in ["L", "R"]:
            assert number % 90 == 0, "Turning must be in 90 degree increments (90, 180, 270 etc)!"
            steps = int(number / 90)
            current = list(self.direction_conversion.keys()).index(self.facing)
            new = current - steps if code == "L" else current + steps
            self.facing = list(self.direction_conversion.keys())[new % 4]
        elif code == "F":
            self.location += self.direction_conversion[self.facing] * number
        else:
            raise ValueError("Wrong code in instruction!")

    def travel(self, instructions):
        start = np.copy(self.location)
        for instruction in instructions:
            self.move(instruction)
        manhattan_distance = np.abs(self.location - start).sum()
        print("Distance travelled:%d." % manhattan_distance)


def part1():
    with open(filename) as fp:
        instructions = [line.strip("\n") for line in fp]
    ship = Ship(location=np.array([0, 0]), facing="E")
    ship.travel(instructions)


class Ship2:
    direction_conversion = OrderedDict({
        "N": np.array([0, 1]),
        "E": np.array([1, 0]),
        "S": np.array([0, -1]),
        "W": np.array([-1, 0])
    })

    def __init__(self, location, waypoint):
        self.location = location
        self.waypoint = waypoint

    def rotate_waypoint(self, degrees):
        radians = 2 * np.pi * degrees / 360
        rotation_matrix = np.array([[np.cos(radians), -np.sin(radians)],
                                    [np.sin(radians), np.cos(radians)]])
        self.waypoint = np.matmul(rotation_matrix, self.waypoint)

    def move(self, instruction):
        code = instruction[0]
        number = int(instruction[1:])
        assert number >= 0, "Number in instruction must be positive!"
        if code in self.direction_conversion.keys():
            self.waypoint += self.direction_conversion[code] * number
        elif code in ["L", "R"]:
            degrees = number if code == "L" else -number
            self.rotate_waypoint(degrees)
        elif code == "F":
            self.location += self.waypoint * number
        else:
            raise ValueError("Wrong code in instruction!")

    def travel(self, instructions):
        start = np.copy(self.location)
        for instruction in instructions:
            self.move(instruction)
        manhattan_distance = np.abs(self.location - start).sum()
        print("Distance travelled:%d." % manhattan_distance)


def part2():
    with open(filename) as fp:
        instructions = [line.strip("\n") for line in fp]
    ship = Ship2(location=np.array([0.0, 0.0]), waypoint=np.array([10.0, 1.0]))
    ship.travel(instructions)


if __name__ == '__main__':
    part1()
    print("***********")
    part2()
