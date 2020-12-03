import numpy as np

def tree_count(arr, i_step=1, j_step=3):
    """Find number of trees along a rational line (trees only tile along second axis)"""
    n, m = arr.shape
    i_inds = np.arange(0, n, i_step)
    j_inds = (i_inds // i_step * j_step) % m

    return arr[i_inds, j_inds].sum()


def day03(inp):
    dat = np.array(list(map(list, inp.splitlines()))) == '#'

    part1 = tree_count(dat)
    part2 = np.prod([tree_count(dat, i_step, j_step) for i_step,j_step in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]])

    return part1, part2


if __name__ == "__main__":
    testinp = open('day03.testinp').read()
    print(day03(testinp))
    inp = open('day03.inp').read()
    print(day03(inp))
