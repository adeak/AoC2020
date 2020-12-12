def day12(inp, part2=False):
    dat = []
    for row in inp.splitlines():
        sdir = row[0]
        dat.append((row[0], int(row[1:])))

    # part 1
    pos = 0j
    if not part2:
        orient = 1 + 0j  # east
    else:
        orient = 10 + 1j # generic waypoint

    for sdir, val in dat:
        if sdir == 'L':
            quarters = val//90
            orient *= (1j) ** quarters 
        elif sdir == 'R':
            quarters = val//90
            orient *= (-1j) ** quarters 
        elif sdir == 'F':
            pos += orient * val
        else:
            deltas = {'N': 1j, 'E': 1, 'S': -1j, 'W': -1}
            delta = deltas[sdir] * val
            if not part2:
                # move the ship
                pos += delta
            else:
                # move the waypoint
                orient += delta

    res = int(abs(pos.real) + abs(pos.imag))

    return res
    

if __name__ == "__main__":
    testinp = open('day12.testinp').read()
    print(day12(testinp))
    print(day12(testinp, part2=True))
    inp = open('day12.inp').read()
    print(day12(inp))
    print(day12(inp, part2=True))
