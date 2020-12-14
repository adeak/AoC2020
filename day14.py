from itertools import product

def day14_part1(inp):
    regs = {}
    for row in inp.splitlines():
        if row.startswith('mask'):
            mask_str = row.split()[-1].lstrip('X')
            # mask: set 1 to 1, 0 to 0
            #       -> | with or_mask of ones, & with and_mask of zeros
            or_mask = int(''.join(c if c == '1' else '0' for c in mask_str), 2) 
            and_mask = int(''.join(c if c == '0' else '1' for c in mask_str), 2)
            continue

        head, *_, tail = row.split()
        val = int(tail)
        index = int(head[4:-1])

        regs[index] = (val | or_mask) & and_mask

    res = sum(regs.values())

    return res

    
def day14_part2(inp):
    # assume that filled indices fit within a reasonably-sized dict...

    regs = {}
    for row in inp.splitlines():
        if row.startswith('mask'):
            mask_str = row.split()[-1]
            or_mask = int(''.join(c if c == '1' else '0' for c in mask_str), 2) 
            float_powers = [exp for exp, c in enumerate(mask_str[::-1]) if c == 'X']

            # handle floaters: gather every potential mask
            or_masks = []
            and_masks = []
            for float_bits in product(range(2), repeat=len(float_powers)):
                float_mask = sum(bit * 2**power for bit, power in zip(float_bits, float_powers))
                float_mask_bits = format(float_mask, '036b')
                aux_or_mask = int(''.join(c if (c == '1' and i in float_powers) else '0' for i, c in enumerate(float_mask_bits[::-1]))[::-1], 2) 
                aux_and_mask = int(''.join(c if (c == '0' and i in float_powers) else '1' for i, c in enumerate(float_mask_bits[::-1]))[::-1], 2) 

                or_masks.append(or_mask | aux_or_mask)
                and_masks.append(aux_and_mask)

            continue

        head, *_, tail = row.split()
        val = int(tail)
        index = int(head[4:-1])

        # handle floaters:
        for or_mask, and_mask in zip(or_masks, and_masks):
            floated_index = (index | or_mask) & and_mask
            regs[floated_index] = val

    res = sum(regs.values())

    return res
    

if __name__ == "__main__":
    testinp = open('day14.testinp').read()
    print(day14_part1(testinp))
    testinp2 = open('day14.testinp2').read()
    print(day14_part2(testinp2))
    inp = open('day14.inp').read()
    print(day14_part1(inp))
    print(day14_part2(inp))
