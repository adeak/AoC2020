def day12(inp):
    dat = []
    for row in inp.splitlines():
        sdir = row[0]
        dat.append((row[0], int(row[1:])))

    # part 1
    pos = 0j
    orient = 1 + 0j  # east
    for sdir, val in dat:
        if sdir == 'L':
            quarters = val//90
            orient *= (1j) ** quarters 
        elif sdir == 'R':
            quarters = val//90
            orient *= (-1j) ** quarters 
        else:
            deltas = {'N': 1j, 'E': 1, 'S': -1j, 'W': -1, 'F': orient}
            delta = deltas[sdir] * val
            pos += delta

    part1 = int(abs(pos.real) + abs(pos.imag))

    return part1
    

def day12_part2(inp):
    dat = []
    for row in inp.splitlines():
        sdir = row[0]
        dat.append((row[0], int(row[1:])))

    # part 2
    wp = 10 + 1j
    pos = 0j
    for sdir, val in dat:
        if sdir == 'L':
            quarters = val//90
            wp *= (1j) ** quarters 
        elif sdir == 'R':
            quarters = val//90
            wp *= (-1j) ** quarters 
        elif sdir == 'F':
            delta = wp * val
            pos += delta
        else:
            deltas = {'N': 1j, 'E': 1, 'S': -1j, 'W': -1}
            delta = deltas[sdir] * val
            wp += delta

    part2 = int(abs(pos.real) + abs(pos.imag))

    return part2
    

if __name__ == "__main__":
    testinp = open('day12.testinp').read()
    print(day12(testinp))
    print(day12_part2(testinp))
    inp = open('day12.inp').read()
    print(day12(inp))
    print(day12_part2(inp))
    # part 1:
    # 434954857400860430790932 too high
    # 11719 too high
