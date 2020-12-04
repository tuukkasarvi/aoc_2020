"""
Part 1. Starting at the top-left corner of your map and following a slope of right 3 and down 1,
how many trees would you encounter?

Part 2.
Time to check the rest of the slopes - you need to minimize the probability of a sudden arboreal stop, after all.

Determine the number of trees you would encounter if, for each of the following slopes, you start at the
top-left corner and traverse the map all the way to the bottom:

Right 1, down 1.
Right 3, down 1. (This is the slope you already checked.)
Right 5, down 1.
Right 7, down 1.
Right 1, down 2.

What do you get if you multiply together the number of trees encountered on each of the listed slopes?
"""
import numpy as np


class Map:
    def __init__(self):
        self.map_array = None

    def read_map(self, filepath):
        with open(filepath) as fp:
            for line in fp:
                line = line.strip('\n')
                if self.map_array is None:
                    self.map_array = np.array(list(line))
                else:
                    self.map_array = np.vstack([self.map_array, list(line)])
                # print(line.strip('\n'))

    def shape(self):
        return self.map_array.shape

    def print(self):
        assert self.map_array is not None, "Read map first!"
        for i in range(len(self.map_array)):
            print("".join(list(self.map_array[i, :])))

    def duplicate_to_right(self, times):
        self.map_array = np.hstack([self.map_array]*times)

    def is_inside(self, location):
        return (location <= (self.map_array.shape - np.array([1, 1]))).all()

    def get_distance_from_borders(self, location):
        return np.hstack([location, (self.map_array.shape - np.array([1, 1])) - location])

    def travel(self, start, vector):
        route = [self.map_array[tuple(start)]]
        location = start + vector
        while self.is_inside(location):
            route += self.map_array[tuple(location)]
            location += vector
        dist = self.get_distance_from_borders(location)
        if (dist[2] < 0) and (dist[3] < 0):
            print("Exited diagonally at %s. Map size: %s " % (location, self.shape()))
        elif dist[2] < 0:
            print("Exited at lower border at %s. Map size: %s " % (location, self.shape()))
        elif dist[3] < 0:
            print("Exited at right border at %s. Map size: %s " % (location, self.shape()))
        else:
            raise ValueError("Something went wrong at exit.")
        return route


def part1():
    map = Map()
    filepath = 'input_3.txt'
    map.read_map(filepath)
    shape = map.shape()
    n_duplications = int(np.ceil(3 * shape[0] / shape[1]))
    map.duplicate_to_right(n_duplications)
    print("Map size:", map.shape())
    route = map.travel(start=np.array([0, 0]), vector=np.array([1, 3]))
    print("Number of trees: %d" % "".join(route).count("#"))


def part2():
    map = Map()
    filepath = 'input_3.txt'
    map.read_map(filepath)
    n_duplications = 100  # enough
    map.duplicate_to_right(n_duplications)
    print("Map size:", map.shape())
    vectors = [
        np.array([1, 1]),
        np.array([1, 3]),
        np.array([1, 5]),
        np.array([1, 7]),
        np.array([2, 1]),
    ]
    answer = 1
    for vector in vectors:
        route = map.travel(start=np.array([0, 0]), vector=vector)
        n_trees = "".join(route).count("#")
        print("Number of trees: %d" % "".join(route).count("#"))
        answer *= n_trees
    print("Answer %d" % answer)


if __name__ == '__main__':
    part1()
    print('**********')
    part2()
