from itertools import product

def day14(inp, no_part2=False):
    regs_p1 = {}
    regs_p2 = {}
    for row in inp.splitlines():
        if row.startswith('mask'):
            mask_str = row.split()[-1]

            # part 1:
            # mask: set 1 to 1, 0 to 0
            #       -> | with or_mask of ones, & with and_mask of zeros
            or_mask = int(''.join(c if c == '1' else '0' for c in mask_str), 2) 
            and_mask_p1 = int(''.join(c if c == '0' else '1' for c in mask_str), 2)

            # part 2:
            # mask: set 1 to 1, X to 0 (added back later)
            and_mask_p2 = int(''.join('0' if c == 'X' else '1' for c in mask_str), 2)
            float_powers = [exp for exp, c in enumerate(mask_str[::-1]) if c == 'X']

            if no_part2:
                # first test case would be bad
                continue

            float_masks = []
            for float_bits in product(range(2), repeat=len(float_powers)):
                float_mask = sum(bit * 2**power for bit, power in zip(float_bits, float_powers))
                float_masks.append(float_mask)

            continue

        head, *_, tail = row.split()
        val = int(tail)
        index = int(head[4:-1])

        # part 1
        regs_p1[index] = (val | or_mask) & and_mask_p1

        if no_part2:
            # first test case would be bad
            continue

        # part 2
        index = (index | or_mask) & and_mask_p2
        for float_mask in float_masks:
            floated_index = index + float_mask
            regs_p2[floated_index] = val

    part1 = sum(regs_p1.values())
    part2 = sum(regs_p2.values())

    return part1, part2
    

if __name__ == "__main__":
    testinp = open('day14.testinp').read()
    print(day14(testinp, no_part2=True)[0])
    testinp2 = open('day14.testinp2').read()
    print(day14(testinp2)[1])
    inp = open('day14.inp').read()
    print(day14(inp))
