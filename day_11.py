"""
1.
Simulate your seating area by applying the seating rules repeatedly until no seats change state.
How many seats end up occupied?

2.
People don't just care about adjacent seats - they care about the first seat they can see in each of those eight
directions!
Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight
directions.

Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an
occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty
seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached,
how many seats end up occupied?

"""
import numpy as np
import cProfile
import pstats
from pstats import SortKey

filename = "data/input_11.txt"


class Map:
    def __init__(self):
        self.map_array = None

    def read_map(self, filepath):
        with open(filepath) as fp:
            for line in fp:
                line = line.strip("\n")
                if self.map_array is None:
                    self.map_array = np.array(list(line))
                else:
                    self.map_array = np.vstack([self.map_array, list(line)])

    def shape(self):
        return self.map_array.shape

    def print(self):
        assert self.map_array is not None, "Read map first!"
        for i in range(len(self.map_array)):
            print("".join(list(self.map_array[i, :])))

    def is_inside(self, location):
        return (location >= 0).all() and (location <= (self.map_array.shape - np.array([1, 1]))).all()


class SeatMap(Map):
    adjacent_vectors = [
        np.array([-1, -1]),
        np.array([-1, 0]),
        np.array([-1, 1]),
        np.array([0, -1]),
        np.array([0, 1]),
        np.array([1, -1]),
        np.array([1, 0]),
        np.array([1, 1]),
    ]

    def get_adjacent(self, point: np.array):
        """ Point (i,j) refers to Map.map_array[i,j]"""
        return [point + v for v in self.adjacent_vectors if self.is_inside(point + v)]

    def get_adjacent_states(self, point: np.array):
        if isinstance(point, np.ndarray):
            return [self.map_array[tuple(p.tolist())] for p in self.get_adjacent(point)]
        else:
            raise ValueError("point needs to be np.darray!")

    def get_updated_state(self, point):
        if isinstance(point, tuple):
            point = np.array(point)
        current_state = self.map_array[tuple(list(point))]
        adjacent_states = self.get_adjacent_states(point)
        if (current_state == "L") and ("#" not in adjacent_states):
            updated_state = "#"
        elif (current_state == "#") and (adjacent_states.count("#") >= 4):
            updated_state = "L"
        else:
            updated_state = current_state
        return updated_state

    def iterate(self):
        """ Returns: False: fixed point. True: not a fixed point."""
        updated_map_array = np.copy(self.map_array)
        for i in range(self.shape()[0]):
            for j in range(self.shape()[1]):
                updated_map_array[i, j] = self.get_updated_state((i, j))
        if (self.map_array == updated_map_array).all():
            return False
        else:
            self.map_array = updated_map_array
            return True

    @staticmethod
    def profile_iterate(self):
        """ Too see what takes time"""
        cProfile.runctx('self.iterate()', globals(), locals(), filename='stats')


def part1():
    map = SeatMap()
    map.read_map(filename)

    profile = False
    if profile:
        map.profile_iterate()
        p = pstats.Stats('stats')
        p.sort_stats(SortKey.CUMULATIVE)
        p.print_stats()

    i = 1
    while map.iterate():
        print("Iteration %d done." % i)
        i += 1
    print("Number of occupied seats %d" % (map.map_array == "#").sum())


class SeatMap2(Map):
    directions = [
        np.array([-1, -1]),
        np.array([-1, 0]),
        np.array([-1, 1]),
        np.array([0, -1]),
        np.array([0, 1]),
        np.array([1, -1]),
        np.array([1, 0]),
        np.array([1, 1]),
    ]

    def get_state(self, point: np.array):
        return self.map_array[tuple(list(point))]

    def get_state_in_direction(self, point, direction):
        x = point + direction
        while self.is_inside(x) and self.get_state(x) == ".":
            x += direction
        if self.is_inside(x):
            return self.get_state(x)
        elif (point == (x - direction)).all():  # point is at border
            return None
        else:  # No chairs encountered
            return self.get_state(x - direction)  # i.e, "."

    def get_seen_states(self, point):
        return [self.get_state_in_direction(point, d) for d in self.directions]

    def get_updated_state(self, point):
        if isinstance(point, tuple):
            point = np.array(point)
        current_state = self.get_state(point)
        seen_states = self.get_seen_states(point)
        if (current_state == "L") and ("#" not in seen_states):
            updated_state = "#"
        elif (current_state == "#") and (seen_states.count("#") >= 5):
            updated_state = "L"
        else:
            updated_state = current_state
        return updated_state

    def iterate(self):
        """ Returns: False: fixed point. True: not a fixed point."""
        updated_map_array = np.copy(self.map_array)
        for i in range(self.shape()[0]):
            for j in range(self.shape()[1]):
                updated_map_array[i, j] = self.get_updated_state((i, j))
        if (self.map_array == updated_map_array).all():
            return False
        else:
            self.map_array = updated_map_array
            return True


def part2():
    map = SeatMap2()
    map.read_map(filename)
    i = 1
    while map.iterate():
        print("Iteration %d done." % i)
        i += 1
    print("Number of occupied seats %d" % (map.map_array == "#").sum())


if __name__ == '__main__':
    part1()
    print("**************")
    part2()
