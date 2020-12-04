"""
While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan
Corporate Authentication System is expecting.

The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job
at the sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second
character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these
positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy
enforcement.

Given the same example list from above:

1-3 a: abcde is valid: position 1 contains a and position 3 does not.
1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
How many passwords are valid according to the new interpretation of the policies?
"""
import re


def parse_line(line: str):
    line_split = line.split(':')
    indices = re.findall(r'\d+', line_split[0])
    i_1 = int(indices[0]) - 1
    i_2 = int(indices[1]) - 1
    character = line_split[0][-1]
    password = line_split[1][1:-1]
    return i_1, i_2, character, password


def is_password_valid(i_1, i_2, character, password):
    return ((password[i_1] == character) + (password[i_2] == character)) == 1


if __name__ == '__main__':
    filename = 'data/input_2.txt'
    with open(filename) as fp:
       n_valid = 0
       for line in fp:
           i_1, i_2, character, password = parse_line(line)
           is_valid = is_password_valid(i_1, i_2, character, password)
           print("{} | {}".format(is_valid, line.strip('\n')))
           n_valid += is_valid
    print('n_valid: %d' % n_valid)
