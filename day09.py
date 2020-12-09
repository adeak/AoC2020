def is_subsum(num, candidate_nums):
    """Check if a number is the sum of two numbers in a set of numbers"""
    for candidate_num in candidate_nums:
        if num - candidate_num in candidate_nums:
            return True
    return False


def day09(inp, preamble=25):
    nums = list(map(int, inp.splitlines()))

    # part 1
    for i in range(preamble, len(nums)):
        num = nums[i]
        candidates = set(nums[i - preamble:i])
        if not is_subsum(num, candidates):
            invalid = num
            break
    part1 = invalid

    # part 2, dumb O(N^2)
    part2 = None
    for i in range(len(nums)):
        cumsum = nums[i]
        for j in range(i + 1, len(nums)):
            cumsum += nums[j]
            if cumsum == invalid:
                # we're done
                ran = nums[i:j+1]
                part2 = max(ran) + min(ran)
                break
            if cumsum > invalid:
                # need to step in i
                break

        if part2:
            break

    return part1, part2


if __name__ == "__main__":
    testinp = open('day09.testinp').read()
    print(day09(testinp, preamble=5))
    inp = open('day09.inp').read()
    print(day09(inp))
