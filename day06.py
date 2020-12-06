from collections import Counter

def day06(inp):
    groups = inp.split('\n\n')  # one string for each group
    counters = [Counter(line.replace('\n', '').replace(' ', '')) for line in groups]  # char count in each group

    part1 = sum(len(counter.keys()) for counter in counters)

    part2 = 0
    for group, counter in zip(groups, counters):
        peeps = len(group.split('\n'))
        part2 += sum(1 for val in counter.values() if val == peeps)

    return part1, part2


if __name__ == "__main__":
    inp = open('day06.inp').read()
    print(day06(inp))
