"""
https://adventofcode.com/2020/day/14

1.
Execute the initialization program. What is the sum of all values left in memory after it completes?

2. Execute the initialization program using an emulator for a version 2 decoder chip.
What is the sum of all values left in memory after it completes?
"""
from abc import ABC, abstractmethod
import re
from copy import deepcopy

filename = "data/input_14.txt"


class Command(ABC):
    def __init__(self, data):
        self.parse(data)

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def execute(self, executor):
        pass


class SetMaskCommand(Command):
    def parse(self, data):
        self.mask = data[(data.find("=") + 1):].strip()

    def execute(self, executor):
        executor.set_mask(self.mask)


class WriteToMemory(Command):
    def parse(self, data):
        self.key = int(re.compile(r"mem\[(\d+)\]").search(data).group(1))
        self.value = int(re.compile(r"= (\d+)$").search(data).group(1))

    def execute(self, executor):
        executor.write_to_memory(self.key, self.value)


class Executor:
    mask_length = 36

    def __init__(self, lines):
        self.commands = [self.parse_command(line) for line in lines]
        self.mask = None
        self.memory = {}

    def set_mask(self, mask):
        self.mask = mask

    @staticmethod
    def mask_bit(bit, mask_char):
        if mask_char == "X":
            return bit
        elif mask_char in ["0", "1"]:
            return mask_char
        else:
            raise ValueError("Unknown mask_char %s" % mask_char)

    def apply_mask(self, value):
        value_36_bits = (("0" * self.mask_length) + bin(value)[2:])[-self.mask_length:]
        masked_value = "".join([self.mask_bit(bit, m) for (bit, m) in zip(value_36_bits, self.mask)])
        masked_value = int(masked_value, 2)
        return masked_value

    def write_to_memory(self, key, value):
        self.memory[key] = self.apply_mask(value)

    @staticmethod
    def parse_command(line):
        if line.startswith("mask"):
            command = SetMaskCommand(line)
        elif line.startswith("mem"):
            command = WriteToMemory(line)
        else:
            raise ValueError("Unknown command: %s!" % line)
        return command

    def execute_all(self):
        for command in self.commands:
            command.execute(self)


def part1():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    executor = Executor(lines)
    executor.execute_all()
    print("Answer: %d" % (sum(executor.memory.values())))


class Memory:
    def __init__(self, address_length):
        self.address_length = address_length
        self.memory = {}

    def set_minus(self, address1, address2):
        """ returns set: address1 - address2 """
        assert len(address1) == len(address2)
        address1 = list(address1)
        address2 = list(address2)
        # Replace "X" in address2 by values in address1. This subset of address2 can only intersect with address1
        address2 = [address2[i] if (address2[i] in ["0", "1"]) else address1[i] for i in range(self.address_length)]
        intersect = all([
            (address1[i] == address2[i]) or (address1[i] == "X") for i in range(self.address_length)
            if (address2[i] in ["0", "1"])
        ])
        if not intersect:
            return ["".join(address1)]
        temp = [i for i in range(self.address_length) if (address1[i] == "X") and (address2[i] in ["0", "1"])]
        if len(temp) == 0:  # address2 covers address1 totally
            return [""]  # empty set
        first_X_in_1_not_in_2 = min(temp)
        # Set first "X" address1 to opposite of 0/1 value in address2
        not_intersecting1 = deepcopy(address1)
        not_intersecting1[first_X_in_1_not_in_2] = str(abs(int(address2[first_X_in_1_not_in_2]) - 1))  # 0->1 and 1->0
        remainder1 = deepcopy(address1)
        # In other branch set it equal. For this branch, use recursion to find out set minus
        remainder1[first_X_in_1_not_in_2] = address2[first_X_in_1_not_in_2]
        return ["".join(not_intersecting1)] + self.set_minus(remainder1, address2)

    def write(self, address, value):
        addresses_in_memory = list(self.memory.keys())
        set_minuses = [self.set_minus(a, address) for a in addresses_in_memory]
        # Remove empty sets "":
        set_minuses = [[a for a in s if a != ""] for s in set_minuses]
        # Update existing memory:
        for i, s in enumerate(set_minuses):
            # Remove old address: value
            val = self.memory[addresses_in_memory[i]]
            del self.memory[addresses_in_memory[i]]
            # Rewrite val to address space not intersecting with new value
            for a in s:
                self.memory[a] = val
        # Insert new overwriting value
        self.memory[address] = value

    def get_address_sum(self, address):
        number_of_addresses = 2**(address.count("X"))
        return number_of_addresses * self.memory[address]

    def get_sum(self):
        return sum([self.get_address_sum(a) for a in self.memory.keys()])


class Executor2:
    mask_length = 36

    def __init__(self, lines):
        self.commands = [self.parse_command(line) for line in lines]
        self.mask = None
        self.memory = Memory(address_length=36)

    def set_mask(self, mask):
        self.mask = mask

    @staticmethod
    def mask_bit(bit, mask_char):
        if mask_char == "0":
            return bit
        elif mask_char in ["1", "X"]:
            return mask_char
        else:
            raise ValueError("Unknown mask_char %s" % mask_char)

    def apply_mask(self, value):
        value_36_bits = (("0" * self.mask_length) + bin(value)[2:])[-self.mask_length:]
        masked_value = "".join([self.mask_bit(bit, m) for (bit, m) in zip(value_36_bits, self.mask)])
        return masked_value

    def write_to_memory(self, address, value):
        masked_address = self.apply_mask(address)
        self.memory.write(masked_address, value)

    @staticmethod
    def parse_command(line):
        if line.startswith("mask"):
            command = SetMaskCommand(line)
        elif line.startswith("mem"):
            command = WriteToMemory(line)
        else:
            raise ValueError("Unknown command: %s!" % line)
        return command

    def execute_all(self):
        for i, command in enumerate(self.commands):
            print(i)
            command.execute(self)

    def get_memory_sum(self):
        return self.memory.get_sum()


def part2():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    executor = Executor2(lines)
    executor.execute_all()
    print("Answer: %d" % executor.get_memory_sum())


if __name__ == "__main__":
    part1()
    print("*****")
    part2()
