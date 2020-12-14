"""
1.
What is the ID of the earliest bus you can take to the airport multiplied by the number of
minutes you'll need to wait for that bus?

2.
What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching
their positions in the list?
"""
import numpy as np

filename = 'data/input_13.txt'


def part1():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    departure_after = int(lines[0])
    buses = [int(item) for item in lines[1].split(",") if item != "x"]
    departures = [departure_after - (departure_after % bus) + bus for bus in buses]
    departure_earliest = min(departures)
    bus = buses[departures.index(departure_earliest)]
    print("Answer %d" % (bus * (departure_earliest - departure_after)))


def is_solution(t, ids, offsets, l):
    """ conditions are of form (t + offset) % ID = 0"""
    return all([((t + offsets[i]) % ids[i]) == 0 for i in range(l)])


def eda(ids, offsets):
    """ It so happens that third offset (17 time units) from t must be divisible by
    643, 17, 13, 29 and 37.
    """
    print([643] + list(np.array(ids)[np.array(ids) == np.abs(np.array(offsets) - 17)]))


def search(ids, offsets, l):
    """ Search over all multiples of 643 * 17 * 13 * 29 * 37 = 152476519.
    Third offset from t must be divisible by 643, 17, 13, 29 and 37.
    (t + 17) % 152476519 = 0.
    """
    a = 152476519
    t = a - 17
    print("Max solution: %d" % np.prod(ids))
    print("Max iterations: %d" % (np.prod(ids) / a))
    print("Average iterations: %d" % (np.prod(ids)/(2*a)))
    while not is_solution(t, ids, offsets, l):
        t += a
        # print(t)
    print("Iterations required: %d" % ((t + 17) / a))
    return t


def part2():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    data = ["x" if item == "x" else int(item) for item in lines[1].split(",")]
    ids = [int(item) for item in lines[1].split(",") if item != "x"]
    offsets = [data.index(id) for id in ids]
    l = len(ids)
    # eda(ids, offsets)
    t = search(ids, offsets, l)
    print("Answer: %d" % t)


if __name__ == '__main__':
    part1()
    print("****")
    part2()
