import numpy as np
from numpy.lib.stride_tricks import as_strided

def day17(inp, num_dims=3):
    state = np.array(list(map(list, inp.splitlines()))) == '#'
    expanded_shape = (None, ) * (num_dims - 2) + (...,)
    state = state[expanded_shape]  # shape (1, nx, ny) or (1, 1, nx, ny)

    for it in range(6):
        # pad with width 2 to get neighbourhood of empty environment
        padded_state = np.pad(state, pad_width=2)  # each dim expanded by 4
        strides = padded_state.strides
        shape = tuple(dim + 2 for dim in state.shape)
        windowed = as_strided(padded_state, shape=shape + (3,) * num_dims, strides=strides*2).copy()
        # this is shaped (nz, nx, ny, 3, 3, 3) or (nw, nz, nx, ny, 3, 3, 3, 3)

        actives = windowed[(...,) + (1,)*num_dims]
        neighbcounts = windowed.sum(tuple(range(num_dims, 2*num_dims)))
        to_inactivate = actives & ~np.isin(neighbcounts, [3, 4])  # include itself in count
        to_activate = ~actives & (neighbcounts == 3)

        # pad with width 1 for next generation
        state = np.pad(state, pad_width=1)
        state[to_inactivate] = False
        state[to_activate] = True

    res = state.sum()

    return res

if __name__ == "__main__":
    testinp = open('day17.testinp').read()
    print(day17(testinp))
    print(day17(testinp, num_dims=4))
    inp = open('day17.inp').read()
    print(day17(inp))
    print(day17(inp, num_dims=4))
