"""
Each of your joltage adapters is rated for a specific output joltage (your puzzle input). Any given adapter
can take an input 1, 2, or 3 jolts lower than its rating and still produce its rated output joltage.

In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the highest-rated adapter
in your bag. (If your adapter list were 3, 9, and 6, your device's built-in adapter would be rated for 12 jolts.)

Treat the charging outlet near your seat as having an effective joltage rating of 0.

Since you have some time to kill, you might as well test all of your adapters. Wouldn't want to get to your resort
and realize you can't even charge your device!

If you use every adapter in your bag at once, what is the distribution of joltage differences between the charging
outlet, the adapters, and your device?

1.
Find a chain that uses all of your adapters to connect the charging outlet to your device's built-in adapter and count
the joltage differences between the charging outlet, the adapters, and your device. What is the number of 1-jolt
differences multiplied by the number of 3-jolt differences?

2.
What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?

"""
import numpy as np


filepath = "data/input_10.txt"


def part1():
    with open(filepath) as fp:
        lines = [line.strip("\n") for line in fp]
    joltages = np.array([int(item) for item in lines])
    joltages.sort()
    joltages = np.concatenate(([0], joltages, [joltages.max() + 3]))
    diffs = joltages[1:] - joltages[:(len(joltages)-1)]
    unique_elements, counts_elements = np.unique(diffs, return_counts=True)
    print(unique_elements)
    answer = counts_elements[0] * counts_elements[1]
    print("Answer %d." % answer)


def get_number_of_paths(ones_group):
    """ For a set of ones [1]_k (k ones) the number of paths f([1]_k) =
    f([1]_(k-1)) + f([1]_(k-2)) + f([1]_(k-3)).
    """
    assert set(ones_group) == {1} or len(ones_group) == 0
    if len(ones_group) == 0:
        return 1
    elif len(ones_group) == 1:
        return 1
    elif len(ones_group) == 2:
        return get_number_of_paths(ones_group[1:]) + get_number_of_paths(ones_group[2:])
    else:  # len >= 3
        return get_number_of_paths(ones_group[1:]) + get_number_of_paths(ones_group[2:]) + \
               get_number_of_paths(ones_group[3:])


def part2():
    with open(filepath) as fp:
        lines = [line.strip("\n") for line in fp]
    joltages = np.array([int(item) for item in lines])
    joltages.sort()
    joltages = np.concatenate(([0], joltages, [joltages.max() + 3]))
    diffs = joltages[1:] - joltages[:(len(joltages)-1)]
    # in diffs there are only 1s and 3s
    # paths can be formed by combining different 1s. Each subset of 1s between 3s is an independent set of paths
    # total number of paths found by multiplying number of paths for each subset of ones: n1 * n2 * n3 ... nk
    diffs_string = "".join([str(i) for i in diffs])
    ones_groups = diffs_string.split("3")
    ones_groups = [list(item) for item in ones_groups]
    ones_groups = [[int(i) for i in item] for item in ones_groups]
    numbers_of_paths = [get_number_of_paths(og) for og in ones_groups]
    total_number_paths = np.prod(np.array(numbers_of_paths))
    print("Answer %d" % total_number_paths)


if __name__ == '__main__':
    part1()
    print("*****")
    part2()
