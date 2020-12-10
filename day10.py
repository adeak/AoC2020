import numpy as np
import scipy.ndimage as ndi

def partition(n):
    """Partition n as the sum of 1, 2, 3"""
    if n == 0:
        return [[]]
    if n == 1:
        return [[1]]
    partitions = []
    for k in [1, 2, 3]:
        if k > n:
            break
        for subpartition in partition(n - k):
            partitions.append([k] + subpartition)
    return partitions


def day10(inp):
    vals = list(map(int, inp.split()))
    vals = [0] + vals + [max(vals) + 3]

    arr = np.array(vals)
    arr.sort()
    diffs = np.diff(arr)
    distrib = np.bincount(diffs)  # count of 0 | 1 | 2 |3 distance
    part1 = distrib[[1, 3]].prod()

    # assert that only distances of 1 or 3 are present
    assert not distrib[[0, 2]].any()

    # for every run of consecutive 1 - 1 distance we can skip some and still work
    #
    # x +1 +1 +1 +1 +1 y
    # x    +2 +1 +1 +1 y
    # x +1    +2 +1 +1 y
    # x +1 +1    +2 +1 y
    # x +1 +1 +1    +2 y
    #
    # x       +3 +1 +1 y
    # x    +2    +2 +1 y
    # ...
    #
    # so for a run of length n we need the number of partitions of n using [1, 2, 3]

    run_slices = ndi.find_objects(ndi.label(diffs == 1)[0])
    run_lengths = [sl.stop - sl.start for sl, in run_slices]

    part2 = np.prod([len(partition(run_length)) for run_length in run_lengths])
    
    return part1, part2


if __name__ == "__main__":
    testinp = open('day10.testinp').read()
    print(day10(testinp))
    inp = open('day10.inp').read()
    print(day10(inp))
