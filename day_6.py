"""
1.
For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?

2.
As you finish the last group's customs declaration, you notice that you misread one word in the instructions:

You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions
to which everyone answered "yes"!
"""

filename = 'data/input_6.txt'


def read_groups():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    groups = []
    group = []
    for line in lines:
        if line == "":
            groups.append(group)
            group = []
        else:
            group.append(line)
    groups.append(group)
    return groups


def get_group_answers_union(group):
    union = set()
    for answer in group:
        union = union | set(list(answer))
    return union


def part1():
    groups = read_groups()
    yes_answers_union = [get_group_answers_union(g) for g in groups]
    ns = [len(y) for y in yes_answers_union]
    print("Answer: %d" % sum(ns))


def get_group_answers_intersection(group):
    intersection = set(list(group[0]))
    for answer in group[1:]:
        intersection = intersection & set(list(answer))
    return intersection


def part2():
    groups = read_groups()
    yes_answers_intersection = [get_group_answers_intersection(g) for g in groups]
    ns = [len(y) for y in yes_answers_intersection]
    print("Answer: %d" % sum(ns))


if __name__ == '__main__':
    part1()
    print("******************")
    part2()
