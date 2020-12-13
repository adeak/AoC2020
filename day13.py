def day13_part1(inp):
    lines = inp.splitlines()
    depart = int(lines[0])
    entries = lines[1].split(',')

    # get moduli
    mods = [int(val) for val in entries if val != 'x']

    # we have to wait at most min(mods) time
    to_check = range(depart, depart + min(mods))
    part1 = None
    for candidate in to_check:
        for mod in mods:
            if not candidate % mod:
                res = (candidate - depart) * mod
                return res
    

def day13_part2(inp):
    entries = inp.splitlines()[-1].split(',')

    modoffsets = {int(val): offset for offset, val in enumerate(entries) if val != 'x'}

    # strategy:
    #    Once found the first match for (mod0, offset0) and (mod1, offset1),
    #    the matching values have a mod0*mod1 cycle
    #
    #    So first find the first match for two moduli,
    #    then start looping mod0*mod1 cycles to find the match for (mod2, offset2)
    #    and repeat as long as we have moduli.
    #
    #    For best performance start searching from largest moduli.

    multiple = max(modoffsets)
    offset = modoffsets.pop(multiple)
    candidate = multiple - offset
    while modoffsets:
        next_mod = max(modoffsets)
        next_offset = modoffsets.pop(next_mod)
        while True:
            if (candidate + next_offset) % next_mod:
                candidate += multiple
            else:
                # we have a new step
                multiple *= next_mod
                break

    return candidate
    

if __name__ == "__main__":
    testinp = open('day13.testinp').read()
    print(day13_part1(testinp))
    print(day13_part2(testinp))
    inp = open('day13.inp').read()
    print(day13_part1(inp))
    print(day13_part2(inp))
