"""
heir password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the Official
Toboggan Corporate Policy that was in effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted
database) and the corporate policy when that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
Each line gives the password policy and then the password. The password policy indicates the lowest and highest number
of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password
 must contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b,
but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits
of their respective policies.

How many passwords are valid according to their policies?
"""
import re


def parse_line(line: str):
    line_split = line.split(':')
    minmax = re.findall(r'\d+', line_split[0])
    min = int(minmax[0])
    max = int(minmax[1])
    character = line_split[0][-1]
    password = line_split[1][1:-1]
    return min, max, character, password


def is_password_valid(min, max, character, password):
    count = password.count(character)
    return (count >= min) and (count <= max)


if __name__ == '__main__':
    filename = 'data/input_2.txt'
    with open(filename) as fp:
       n_valid = 0
       for line in fp:
           min, max, character, password = parse_line(line)
           is_valid = is_password_valid(min, max, character, password)
           print("{} | {}".format(is_valid, line.strip('\n')))
           n_valid += is_valid
    print('n_valid: %d' % n_valid)
