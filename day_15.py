"""
https://adventofcode.com/2020/day/15
1.
Given your starting numbers, what will be the 2020th number spoken?

2.
Given your starting numbers, what will be the 30000000th number spoken?
"""
puzzle_input = [17, 1, 3, 16, 19, 0]


def get_next_number(sequence):
    current_index = len(sequence) - 1
    indices = [i for i, number in enumerate(sequence[:-1]) if number == sequence[-1]]
    if len(indices) == 0:
        next_number = 0
    else:
        next_number = current_index - indices[-1]
    return sequence + [next_number]


def part1():
    n_iterations = 2020 - len(puzzle_input)
    sequence = puzzle_input
    for i in range(n_iterations):
        sequence = get_next_number(sequence)
    print("Answer: %d" % sequence[-1])


class SequenceMemory:
    def __init__(self, sequence):
        self.memory = {}
        self.last_number = None
        self.last_index = None
        self.load_sequence(sequence)

    def load_sequence(self, sequence):
        for n in sequence[:-1]:
            max_index = max([i for i, number in enumerate(sequence) if number == n])
            self.memory[n] = max_index
        self.last_number = sequence[-1]
        self.last_index = len(sequence) - 1

    def iterate(self):
        if self.last_number in self.memory.keys():
            next_number = self.last_index - self.memory[self.last_number]
        else:
            next_number = 0
        self.memory[self.last_number] = self.last_index
        self.last_index += 1
        self.last_number = next_number

    def get_last_number(self):
        return self.last_number


def part2():
    target_number = 30000000
    n_iterations = target_number - len(puzzle_input)
    sequence = puzzle_input
    sequence_memory = SequenceMemory(sequence)
    for i in range(n_iterations):
        sequence_memory.iterate()
        print(i)
    print("Answer: %d" % sequence_memory.get_last_number())


if __name__ == "__main__":
    part1()
    print("***********")
    part2()
