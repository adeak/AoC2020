from itertools import count
import numpy as np
from numpy.lib.stride_tricks import as_strided

def day11(inp, part2=False):
    # map: 0 for floor, 1 for empty seat
    state = (np.array(list(map(list, inp.splitlines()))) == 'L').astype(int)

    # pad with border of floor
    padded_state = np.pad(state, 1)
    n, m = padded_state.shape

    last = padded_state.copy()
    for it in count():
        # iterate a step
        if not part2:
            state = padded_state[1:-1, 1:-1]
            occupieds = state == 2
            empties = state == 1

            strides = padded_state.strides
            windowed = as_strided(padded_state, shape=state.shape + (3, 3), strides=strides*2).copy()
    
            # avoid self-interaction
            windowed[..., 1, 1] = 0

            to_occupy = empties & ((windowed == 2).sum((-2, -1)) == 0)
            to_vacate = occupieds & ((windowed == 2).sum((-2, -1)) >= 4)
            state[to_occupy] = 2
            state[to_vacate] = 1
        else:
            # dumb loop :(
            occupieds = padded_state == 2
            empties = padded_state == 1
            directions = np.array([
                (0, 1),
                (1, 1),
                (1, 0),
                (1, -1),
                (0, -1),
                (-1, -1),
                (-1, 0),
                (-1, 1)
            ])
            next_state = padded_state.copy()
            for i, j in zip(*(padded_state > 0).nonzero()):
                occ_count = 0
                for orient in directions:
                    pos = np.array([i, j])
                    while True:
                        pos += orient
                        if not (0 <= pos[0] < n and 0 <= pos[1] < m):
                            break
                        this_state = padded_state[tuple(pos)]
                        if not this_state:
                            continue
                        occ_count += this_state == 2
                        break

                if empties[i, j] and occ_count == 0:
                    next_state[i, j] = 2
                if occupieds[i, j] and occ_count >= 5:
                    next_state[i, j] = 1

            padded_state[...] = next_state

        if np.array_equal(padded_state, last):
            res = (padded_state == 2).sum()
            break
        
        last = padded_state.copy()

    return res
    


if __name__ == "__main__":
    testinp = open('day11.testinp').read()
    print(day11(testinp))
    testinp = open('day11.testinp').read()
    print(day11(testinp, part2=True))
    inp = open('day11.inp').read()
    print(day11(inp))
    inp = open('day11.inp').read()
    print(day11(inp, part2=True))
