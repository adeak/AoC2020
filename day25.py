from itertools import count


def transform(subject, target=None, n_loops=float('inf')):
    """Transform a subject until target is found or a given number of times"""
    res = 1
    loop = 0
    while True:
        loop += 1
        res *= subject
        res %= 20201227

        if res == target or loop == n_loops:
            break

    return loop, res


def day25(inp):
    door_key, card_key = list(map(int, inp.splitlines()))

    door_loops, _ = transform(7, target=door_key)
    _, encryption_key = transform(card_key, n_loops=door_loops)

    return encryption_key


if __name__ == "__main__":
    testinp = open('day25.testinp').read()
    print(day25(testinp))
    inp = open('day25.inp').read()
    print(day25(inp))
