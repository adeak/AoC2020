from itertools import count
from collections import defaultdict, deque

def day15(inp, maxiter=2020):
    """Brute force for now :( ~ 3 GB RAM is enough"""
    *nums, = map(int, inp.strip().split(','))

    last_turns = defaultdict(lambda: deque(maxlen=2))
    for i, num in enumerate(nums):
        last_turns[num].append(i)
    last_num = nums[-1]

    for i in range(len(nums), maxiter):
        lasts_now = last_turns[last_num]
        if len(lasts_now) == 1:
            # first time spoken
            spoken_now = 0
        else:
            spoken_now = lasts_now[-1] - lasts_now[0]
    
        last_turns[spoken_now].append(i)
        last_num = spoken_now

    part1 = spoken_now

    return part1


if __name__ == "__main__":
    testinp = open('day15.testinp').read()
    print(day15(testinp))
    print(day15(testinp, maxiter=30_000_000))
    inp = open('day15.inp').read()
    print(day15(inp))
    print(day15(inp, maxiter=30_000_000))
