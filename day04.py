import re

def day04(inp):
    # put each entry on a single line and parse
    rows = re.sub('\n(?!\n)', ' ', inp).splitlines()
    dat = [dict(entry.split(':') for entry in row.split()) for row in rows]

    # callable constraints for each mandatory key
    reqs = {'byr': lambda n: int(n) in range(1920, 2002 + 1),
            'iyr': lambda n: int(n) in range(2010, 2020 + 1),
            'eyr': lambda n: int(n) in range(2020, 2030 + 1),
            'hgt': lambda L: (L.endswith('cm') and int(L[:-2]) in range(150, 193 + 1))
                             or (L.endswith('in') and int(L[:-2]) in range(59, 76 + 1)),
            'hcl': lambda c: re.match('#[0-9a-f]{6}$', c),
            'ecl': lambda c: c in 'amb blu brn gry grn hzl oth'.split(),
            'pid': lambda p: re.match('[0-9]{9}$', p),
            }

    part1 = sum(1 for d in dat if d.keys() >= reqs.keys())
    part2 = sum(1 for d in dat if all(req(d.get(key, '-1')) for key, req in reqs.items()))

    return part1, part2

if __name__ == "__main__":
    testinp = open('day04.testinp').read()
    print(day04(testinp)[0])
    testinp2 = open('day04.testinp2').read()
    print(day04(testinp2)[1])
    inp = open('day04.inp').read()
    print(day04(inp))
