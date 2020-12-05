import numpy as np

def decode_seat(word):
    """Decode 10-length seat code, return seat ID."""
    head, tail = word[:7], word[7:]

    row = int(''.join(['1' if c == 'B' else '0' for c in head]), 2)
    col = int(''.join(['1' if c == 'R' else '0' for c in tail]), 2)
    seat = 8*row + col

    return seat

def day05(inp):
    words = inp.splitlines()
    seats = np.array([decode_seat(word) for word in words])
    part1 = seats.max()  # max ID
    part2 = (set(range(seats.min(), seats.max() + 1)) - set(seats)).pop()  # only gap in IDs

    return part1, part2

if __name__ == "__main__":
    testinp = open('day05.testinp').read()
    print(day05(testinp)[0])
    inp = open('day05.inp').read()
    print(day05(inp))
