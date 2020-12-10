"""
1.
The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble)
which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?


2.
The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a
contiguous set of at least two numbers in your list which sum to the invalid number from step 1.

To find the encryption weakness, add together the smallest and largest number in this contiguous range;
in this example, these are 15 and 47, producing 62.

What is the encryption weakness in your XMAS-encrypted list of numbers?
"""
import numpy as np


filepath = "data/input_9.txt"


class Checker:
    def __init__(self, numbers, preamble_size):
        self.numbers = numbers
        self.preamble_size = preamble_size
        self.cursor = preamble_size

    def check_if_ok(self):
        preceding_numbers = self.numbers[(self.cursor - self.preamble_size):self.cursor]
        all_sums = np.reshape(preceding_numbers, (self.preamble_size, 1)) + \
                   np.reshape(preceding_numbers, (1, self.preamble_size))
        return (all_sums == self.numbers[self.cursor]).any()


def part1():
    with open(filepath) as fp:
        lines = [line.strip("\n") for line in fp]
    numbers = np.array([int(item) for item in lines])
    checker = Checker(numbers, 25)
    while checker.check_if_ok():
        checker.cursor += 1

    answer = checker.numbers[checker.cursor]
    print("Answer: %d" % answer)
    return answer


def is_sum_of_contiguous_numbers(target, numbers, group_length):
    group_sums = np.array([sum(numbers[i:(i + group_length)]) for i in range(len(numbers) - group_length + 1)])
    is_sum = (group_sums == target).any()
    if is_sum:
        # return indices of numbers that sum up to target
        return np.where(group_sums == target)[0] + np.array(range(group_length))
    else:
        return False


def part2(answer_1):
    with open(filepath) as fp:
        lines = [line.strip("\n") for line in fp]
    numbers = [int(item) for item in lines]

    group_length = 2
    indices = is_sum_of_contiguous_numbers(answer_1, numbers, group_length)
    while not isinstance(indices, np.ndarray):
        group_length += 1
        indices = is_sum_of_contiguous_numbers(answer_1, numbers, group_length)

    contiguous_range = np.array(numbers)[indices]
    print("Contiguous range %s" % contiguous_range)
    print("Answer %d" % (min(contiguous_range) + max(contiguous_range)))


if __name__ == '__main__':
    answer_1 = part1()
    print("*******")
    part2(answer_1)
