"""
1.
How many bag colors can eventually contain at least one shiny gold bag?
(The list of rules is quite long; make sure you get all of it.)

2.
How many individual bags are required inside your single shiny gold bag?
"""
filename = 'data/input_7.txt'


def parse_rules(lines):
    rules = {}
    for line in lines:
        # print(line)
        line = line.replace("bags", "")
        line = line.replace("bag", "")
        line = line.replace(".", "")
        key = line.split('contain')[0].strip()
        values_data = [item.strip() for item in line.split('contain')[1].split(",")]
        if len(values_data) == 1 and values_data[0] == 'no other':
            rules[key] = []
        else:
            rules[key] = [(int(data[0]), data[2:]) for data in values_data]
    return rules


def can_contain(bags: set, rules):
    """ Return set of bags that can contain at least one of the bags in bags argument"""
    return {parent for parent in rules.keys() if (bags & {children_counts[1] for children_counts in rules[parent]})}


def can_contain_multistep(bags: set, rules):
    """ Return set of bags that can contain any of the bags in bags argument"""
    parents = can_contain(bags, rules)
    ancestors = bags | parents
    if bags == ancestors:
        return bags  # or ancestors
    else:
        return can_contain_multistep(ancestors, rules)


def part1():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    rules = parse_rules(lines)
    from pprint import pprint
    pprint(rules)
    ancestors = can_contain_multistep({"shiny gold"}, rules) - {"shiny gold"}
    print("Answer %d " % len(ancestors))


def number_of_bags_inside(bag, rules):
    return sum([child[0]*(1 + number_of_bags_inside(child[1], rules)) for child in rules[bag]])


def part2():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    rules = parse_rules(lines)
    answer = number_of_bags_inside("shiny gold", rules)
    print("Answer %d " % answer)


if __name__ == '__main__':
    part1()
    print("*********")
    part2()
