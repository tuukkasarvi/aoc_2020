"""
https://adventofcode.com/2020/day/16

1. Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?

2. Once you work out which field is which, look for the six fields on your ticket that start with the word departure.
What do you get if you multiply those six values together?
"""
import re
import numpy as np
from typing import NamedTuple

filename = "data/input_16.txt"


class MinMaxRule(NamedTuple):
    min: int
    max: int


class Field:
    def __init__(self, data):
        self.name = re.compile(r"^(.+):").search(data).group(1)
        numbers = re.findall(r"(\d+)", data)
        self.rule1 = MinMaxRule(min=int(numbers[0]), max=int(numbers[1]))
        self.rule2 = MinMaxRule(min=int(numbers[2]), max=int(numbers[3]))

    def is_number_valid(self, number):
        return ((number >= self.rule1.min) and (number <= self.rule1.max)) or \
               ((number >= self.rule2.min) and (number <= self.rule2.max))


class Ticket:
    def __init__(self, data):
        self.numbers = [int(n) for n in data.split(",")]
        assert len(self.numbers) == 20

    def get_invalid(self, fields):
        """Get numbers that are not valid for any field"""
        return [n for n in self.numbers if not (any([field.is_number_valid(n) for field in fields]))]

    def get_numbers(self):
        return self.numbers


def part1():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    line_no_your_ticket = lines.index("your ticket:")
    line_no_nearby_tickets = lines.index("nearby tickets:")
    field_data = lines[:(line_no_your_ticket - 1)]
    your_ticket_data = lines[(line_no_your_ticket + 1)]
    nearby_tickets_data = lines[(line_no_nearby_tickets + 1):]
    fields = [Field(line) for line in field_data]
    your_ticket = Ticket(your_ticket_data)
    nearby_tickets = [Ticket(data) for data in nearby_tickets_data]

    invalid_numbers = [ticket.get_invalid(fields) for ticket in nearby_tickets]
    invalid_numbers_flat = [n for invalid in invalid_numbers for n in invalid]
    print("Answer: %d" % sum(invalid_numbers_flat))


def unpack_list(l):
    """ Not in use."""
    if isinstance(l, list):
        for a in l:
            for b in unpack_list(a):
                yield b
    else:
        yield l


def remove_row_and_col_from_matrix(matrix, row_number, col_number):
    mat = matrix.copy()
    mat = np.delete(mat, (row_number), axis=0)
    mat = np.delete(mat, (col_number), axis=1)
    return mat


def iterate_solution(solutions, is_valid_matrix, fields, positions):
    """ This is a combinatorial problem with feasibility constraints. Solve with ad hoc algorithm
    In matrix, a_ij = is jth position possible for ith field (fields[i])
    """
    n_possible = is_valid_matrix.sum(axis=1)
    chosen_field_i = np.argwhere(n_possible == min(n_possible))[0][0]
    possible_positions_j = [x[0] for x in np.argwhere(is_valid_matrix[chosen_field_i, :])]
    if len(possible_positions_j) == 0:
        return []
    elif len(possible_positions_j) == 1:
        if is_valid_matrix.shape == (1, 1):
            return {**solutions, fields[chosen_field_i].name: positions[possible_positions_j[0]]}
        else:
            return iterate_solution(
                {**solutions, fields[chosen_field_i].name: positions[possible_positions_j[0]]},
                remove_row_and_col_from_matrix(is_valid_matrix, chosen_field_i, possible_positions_j[0]),
                fields[0:chosen_field_i] + fields[(chosen_field_i + 1):],
                positions[0:possible_positions_j[0]] + positions[(possible_positions_j[0] + 1):]
            )
    else:
        return [iterate_solution(
            {**solutions, fields[chosen_field_i].name: positions[j]},
            remove_row_and_col_from_matrix(is_valid_matrix, chosen_field_i, j),
            fields[0:chosen_field_i] + fields[(chosen_field_i + 1):],
            positions[0:j] + positions[(j + 1):]
        )
            for j in possible_positions_j]


def part2():
    with open(filename) as fp:
        lines = [line.strip("\n") for line in fp]
    line_no_your_ticket = lines.index("your ticket:")
    line_no_nearby_tickets = lines.index("nearby tickets:")
    field_data = lines[:(line_no_your_ticket - 1)]
    your_ticket_data = lines[(line_no_your_ticket + 1)]
    nearby_tickets_data = lines[(line_no_nearby_tickets + 1):]
    fields = [Field(line) for line in field_data]
    your_ticket = Ticket(your_ticket_data)
    nearby_tickets = [Ticket(data) for data in nearby_tickets_data]
    invalid_numbers = [ticket.get_invalid(fields) for ticket in nearby_tickets]
    invalid_tickets_indices = [i for i in range(len(invalid_numbers)) if len(invalid_numbers[i]) > 0]

    # Discard invalid from part 1
    updated_nearby_tickets = [nearby_tickets[i] for i in range(len(nearby_tickets)) if i not in invalid_tickets_indices]
    print("After discarding invalid tickets from part 1 %d tickets remain." % len(updated_nearby_tickets))

    # Get a boolean matrix where a_{i,j} tells if location j (1-20) could be possibly fields[i]
    n_fields = len(fields)
    is_valid_matrix = np.zeros((n_fields, n_fields), dtype=bool)
    for i, field in enumerate(fields):
        for j in range(len(fields)):
            is_valid_matrix[i, j] = all([field.is_number_valid(ticket.get_numbers()[j])
                                         for ticket in updated_nearby_tickets])

    solution = iterate_solution({}, is_valid_matrix, fields, list(range(len(fields))))

    departure_field_names = [f.name for f in fields if f.name.startswith("departure")]
    departure_field_locations = [solution[name] for name in departure_field_names]
    your_ticket_numbers = your_ticket.get_numbers()
    answer = np.prod([your_ticket_numbers[l] for l in departure_field_locations])
    print("Answer: %d" % answer)


if __name__ == "__main__":
    part1()
    print("*******")
    part2()
