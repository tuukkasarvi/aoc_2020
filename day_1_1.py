"""
Day 1. Part 1.
Of course, your expense report is much larger. Find the two entries that sum to 2020;
what do you get if you multiply them together?
"""
import numpy as np
filename = 'input.txt'

if __name__ == '__main__':
    data = np.genfromtxt(filename)
    matrix = np.array([data]*len(data))
    sum_matrix = matrix + np.transpose(matrix)
    indices = np.where(sum_matrix == 2020)[0]
    assert data[indices[0]] + data[indices[1]] == 2020
    print('Answer %d' % (data[indices[0]] * data[indices[1]]))
