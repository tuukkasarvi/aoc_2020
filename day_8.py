"""
--- Day 8: Handheld Halting ---
Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the
in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting
next to you.

Their handheld game console won't turn on! They ask if you can take a look.

You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should
be able to fix it, but first you need to be able to run the code in isolation.

The boot code is represented as a text file with one instruction per line of text. Each instruction consists of
an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

acc increases or decreases a single global value called the accumulator by the value given in the argument. For
example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the
instruction immediately below it is executed next.
jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument
as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue
to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
For example, consider the following program:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
These instructions are visited in this order:

nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |
First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next
 instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes,
 setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to
  continue back at the first acc +1.

This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries
to run any instruction a second time, you know it will never terminate.

Immediately before the program would run an instruction a second time, the value in the accumulator is 5.

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in
the accumulator?

2.
Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the
value of the accumulator after the program terminates?
"""
from typing import NamedTuple
from copy import deepcopy

filename = 'data/input_8.txt'


class Executor:
    def __init__(self, commands):
        self.commands = commands
        self.cursor = 0
        self.accumulator = 0
        self.history = []
        self.status = None

    def reset(self):
        self.cursor = 0
        self.accumulator = 0
        self.history = []
        self.status = None

    def execute(self):
        if self.cursor in self.history:
            self.status = "Same command is about to be run again. Aborting. Accumulator value is %d" % self.accumulator
            return False
        elif self.cursor >= len(self.commands):
            self.status = "End of program."
            return False
        else:
            self.history.append(self.cursor)
        command = self.commands[self.cursor]
        if command.name == 'acc':
            self.accumulator += command.value
            self.cursor += 1
        elif command.name == 'jmp':
            self.cursor += command.value
        elif command.name == 'nop':
            self.cursor += 1
        else:
            raise ValueError("Unknown command!")
        return True

    def run(self, verbose=True):
        self.reset()
        self.status = 'running'
        while self.execute():
            pass
        if verbose:
            print(self.status)

    def flip_command(self, index):
        if self.commands[index].name == 'jmp':
            new_command = Command(name='nop', value=self.commands[index].value)
        elif self.commands[index].name == 'nop':
            new_command = Command(name='jmp', value=self.commands[index].value)
        else:
            raise ValueError("Trying to flip acc. Not allowed.")
        self.commands[index] = new_command

    def run2(self):
        original_commands = deepcopy(self.commands)
        ind_jmp_or_nop = [i for i in range(len(self.commands)) if self.commands[i].name in ['jmp', 'nop']]
        edit_cursor = -1
        while self.status != "End of program.":
            edit_cursor += 1
            self.commands = deepcopy(original_commands)
            self.flip_command(ind_jmp_or_nop[edit_cursor])
            self.run(verbose=False)
        print(self.status)
        print("Accumulator value is %d" % self.accumulator)


class Command(NamedTuple):
    name: str
    value: int


def parse_commands(lines):
    return [Command(name=line[:3], value=int(line[4:])) for line in lines]


def part1():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    commands = parse_commands(lines)
    executor = Executor(commands=commands)
    executor.run()


def part2():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    commands = parse_commands(lines)
    executor = Executor(commands=commands)
    executor.run2()


if __name__ == '__main__':
    part1()
    print("******")
    part2()
