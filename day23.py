from itertools import chain, tee

def day23(inp, part1=True):
    # use a dict as a linked list, ugh (had to look this up after 6+ hours of struggle)
    cups_start = list(map(int, inp.strip()))
    if part1:
        cups = cups_start + cups_start[:1]
        n_moves = 100
    else:
        cups = chain(cups_start, range(len(cups_start) + 1, 1000_001), cups_start[:1])
        n_moves = 10_000_000
    thisiter, nextiter = tee(cups)
    next(nextiter)

    # ld as in linked dict
    cups_ld = dict(zip(thisiter, nextiter))
    mincup, maxcup = min(cups_ld), max(cups_ld)

    current = next(iter(cups_ld))
    for move in range(n_moves):
        old_current = current
        picks = []
        for _ in range(3):
            pick = cups_ld[current]
            picks.append(pick)
            current = pick
        current = cups_ld[current]
        destination = old_current
        while True:
            destination -= 1
            if destination < mincup:
                destination = maxcup
            if destination not in picks:
                break

        cups_ld[picks[-1]] = cups_ld[destination]
        cups_ld[old_current] = current
        cups_ld[destination] = picks[0]

    if part1:
        cups = []
        cup = 1
        while True:
            cup = cups_ld[cup]
            if cup == 1:
                break
            cups.append(cup)
        res = ''.join(map(str, cups))
    else:
        first = cups_ld[1]
        second = cups_ld[first]
        res = first * second

    return res


if __name__ == "__main__":
    testinp = open('day23.testinp').read()
    print(day23(testinp))
    print(day23(testinp, part1=False))
    inp = open('day23.inp').read()
    print(day23(inp))
    print(day23(inp, part1=False))
