from collections import defaultdict

import numpy as np  # due to sheer laziness

def splitter(s):
    """Yield separated blocks of a direction string"""
    it = iter(s)
    for c in it:
        if c in 'ew':
            yield c
        else:
            yield c + next(it)


def day24(inp):
    lines = inp.splitlines()
    lineiters = map(splitter, lines)

    # mapping from letter to 3-axis coordinate: (axes are along 0, 120 and 240 degree directions)
    steps = {
        'e': (1, 0, 0),
        'w': (-1, 0, 0),
        'nw': (0, 1, 0),
        'se': (0, -1, 0),
        'sw': (0, 0, 1),
        'ne': (0, 0, -1),
    }

    # initial state (part1):
    tiles = defaultdict(bool)  # default False is white
    for it in lineiters:
        pos = np.array([0, 0, 0])
        for c in it:
            step = steps[c]
            pos += step
        # normalize position: push z index to 0
        pos -= pos[-1]
        tiles[tuple(pos)] = not tiles[tuple(pos)]

    part1 = sum(tiles.values())

    # part 2: simulate
    for step in range(100):
        # propagate blackness to neighbours to count, this way we get increasing sets
        black_counts = defaultdict(int)
        for pos, is_black in tiles.items():
            # initialize "this" tile if necessary for looping logistics later
            black_counts[pos]

            if is_black:
                # increase "black neighbour" count on all 6 neighbours
                position = np.array(pos)
                for dir in steps.values():
                    other_pos = position + dir
                    other_pos -= other_pos[-1]
                    black_counts[tuple(other_pos)] += 1

        old_tiles = tiles
        tiles = old_tiles.copy()

        for pos, black_neighbs in black_counts.items():
            is_black = old_tiles[pos]
            if is_black and (black_neighbs == 0 or black_neighbs > 2):
                # turn white
                tiles[pos] = False
            elif not is_black and black_neighbs == 2:
                # turn black
                tiles[pos] = True

    part2 = sum(tiles.values())

    return part1, part2


if __name__ == "__main__":
    testinp = open('day24.testinp').read()
    print(day24(testinp))
    inp = open('day24.inp').read()
    print(day24(inp))
