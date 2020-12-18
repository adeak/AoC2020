import operator
from functools import partial

def parse(line):
    """Parse a line using the weird rules

    Assumption: every literal is a single-digit integer
    """
    stack = []
    line = line.strip().replace(' ', '')
    this_group = []  # always have an enclosing group
    stack.append(this_group)

    for token in line:
        if token.isdigit():
            val = int(token)
            if not this_group:
                # start of the line
                this_group.append(val)
            else:
                # apply an operation
                # previous value on the stack is a curried function
                op = this_group.pop()
                this_group.append(op(val))
        elif token == '(':
            # start a new level on the stack
            this_group = []
            stack.append(this_group)
        elif token == ')':
            # end a new level on the stack
            that_group = stack.pop()  # should be this_group
            this_group = stack[-1]
            val = that_group.pop()

            if this_group and callable(this_group[-1]):
                # trivial enclosing group at worst
                op = this_group.pop()
                this_group.append(op(val))
            else:
                this_group.append(val)
        else:
            ops = {'+': operator.add, '*': operator.mul}
            op = ops[token]
            first_arg = this_group.pop()
            this_group.append(partial(op, first_arg))

    ans = stack[0][0]
    return ans


def parenthesize(line):
    """Add parentheses around additions for part 2 (thanks to a tip from @ztane)"""

    line = line.replace(' ', '')
    num_plusses = line.count('+')
    last_index = 0
    transformed = list(line)
    for _ in range(num_plusses):
        #next_plus = next(i + last_index for i, c in enumerate(transformed) if c == '+')
        next_plus = transformed.index('+', last_index)
        last_index = next_plus + 2

        # add a starting parenthesis
        if transformed[next_plus - 1] != ')':
            # previous token is a number, we can just prepend an opening parenthesis
            insert_index = next_plus - 1
        else:
            # we need to find the first opening parenthesis
            # count parentheses to balance them
            paren_count = 0
            for i in range(next_plus - 1, -1, -1):
                c = transformed[i]
                if c == ')':
                    paren_count += 1
                elif c == '(':
                    paren_count -= 1
                    if not paren_count:
                        insert_index = i
                        break
        transformed.insert(insert_index, '(')
        next_plus += 1

        # find its matching ending parenthesis
        if transformed[next_plus + 1] != '(':
            insert_index = next_plus + 2
        else:
            # count parentheses to balance them
            paren_count = 0
            for i, c in enumerate(transformed[next_plus + 1 :], start=next_plus + 1):
                if c == '(':
                    paren_count += 1
                elif c == ')':
                    paren_count -= 1
                    if not paren_count:
                        insert_index = i + 1
                        break
        transformed.insert(insert_index, ')')

    return ''.join(transformed)


def day18(inp):
    part1 = sum(parse(line) for line in inp.splitlines())
    part2 = sum(parse(parenthesize(line)) for line in inp.splitlines())

    return part1, part2


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(day18(testinp))
    inp = open('day18.inp').read()
    print(day18(inp))
