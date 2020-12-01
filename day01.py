import numpy as np

def day01(inp):
    nums_raw = np.fromstring(inp, sep=' ').astype(int)
    nums = set(nums_raw)

    # make sure we didn't lose any duplicates
    assert len(nums) == nums_raw.size

    part1 = part2 = None
    for num in nums:
        if not part1 and 2020 - num in nums:
            # find a matching number to add up to 2020
            part1 = num * (2020 - num)
        
        if not part2:
            # loop over every other number and find a potential match
            for num2 in nums - {num}:
                if 2020 - num - num2 in nums:
                    part2 = num * num2 * (2020 - num - num2)
                    break

        if part1 and part2:
            break

    return part1, part2

if __name__ == "__main__":
    inp = open('day01.inp').read()
    print(day01(inp))
