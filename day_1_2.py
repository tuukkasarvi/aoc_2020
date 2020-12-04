"""
Day 1. Part 2.
The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left
over from a past vacation. They offer you a second one if you can find three numbers in your expense report
that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying
them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?
"""
import numpy as np
# folder = 'aoc_2020/'
filename = 'input.txt'

if __name__ == '__main__':
    data = np.genfromtxt(filename)
    a1 = np.reshape(data, (len(data), 1, 1))
    a2 = np.reshape(data, (1, len(data), 1))
    a3 = np.reshape(data, (1, 1, len(data)))
    # automatic broadcasting
    tensor = a1 + a2 + a3
    indices = np.where(tensor == 2020)
    indices = (indices[0][0], indices[1][0], indices[2][0])
    assert data[indices[0]] + data[indices[1]] + data[indices[2]] == 2020
    print('Answer %d' % (data[indices[0]] * data[indices[1]] * data[indices[2]]))
