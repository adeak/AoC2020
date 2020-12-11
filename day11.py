from itertools import count
import numpy as np
from numpy.lib.stride_tricks import as_strided

def day11_part1(inp):
    # map: 0 for floor, 1 for empty seat
    state = (np.array(list(map(list, inp.splitlines()))) == 'L').astype(int)

    # pad with border of floor
    padded_state = np.pad(state, 1)
    n, m = padded_state.shape

    last = padded_state.copy()
    for it in count():
        # iterate a step
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

        if np.array_equal(padded_state, last):
            res = (padded_state == 2).sum()
            break
        
        last = padded_state.copy()

    return res
    

def day11_part2(inp):
    # map: 0 for floor, 1 for empty seat
    state = (np.array(list(map(list, inp.splitlines()))) == 'L').astype(int)

    # pad with border of floor
    padded_state = np.pad(state, 1)
    n, m = padded_state.shape

    # get adjacency: (k, 8, 2)-shaped if there are k seats
    seats = (padded_state > 0).nonzero()
    n_seats = seats[0].size
    adj = np.empty((n_seats, 8, 2), dtype=int)
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
    for i_seat, (i, j) in enumerate(zip(*seats)):
        for k, orient in enumerate(directions):
            pos = np.array([i, j])
            while True:
                pos += orient
                if not (0 <= pos[0] < n and 0 <= pos[1] < m):
                    adj[i_seat, k, :] = pos - orient  # guaranteed empty
                    break
                this_state = padded_state[tuple(pos)]
                if this_state:
                    # this is the first visible seat
                    adj[i_seat, k, :] = pos
                    break

    # iterate, use adjacency information
    last = padded_state.copy()
    for it in count():
        occupieds = padded_state == 2
        empties = padded_state == 1
        next_state = padded_state.copy()
        for i_seat, (i, j) in enumerate(zip(*seats)):
            adjacents = padded_state[adj[i_seat, :, 0], adj[i_seat, :, 1]]
            occ_count = (adjacents == 2).sum()

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
    print(day11_part1(testinp))
    testinp = open('day11.testinp').read()
    print(day11_part2(testinp))
    inp = open('day11.inp').read()
    print(day11_part1(inp))
    inp = open('day11.inp').read()
    print(day11_part2(inp))
