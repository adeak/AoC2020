import operator
from functools import partial
import string

from pyparsing import infixNotation, oneOf, opAssoc, pyparsing_common

def parse_part1(line):
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


def parse_part2(line):
    """Do part 2 using pyparsing, based on https://stackoverflow.com/a/23956778"""

    def add_toks(s, loc, tokens):
            return tokens[0][0] + tokens[0][-1]
    def mul_toks(s, loc, tokens):
            return tokens[0][0] * tokens[0][-1]

    operand = pyparsing_common.integer
    expr = infixNotation(operand,
        [
        (oneOf('+'), 2, opAssoc.RIGHT, add_toks),
        (oneOf('*'), 2, opAssoc.RIGHT, mul_toks),
        ])

    return expr.parseString(line)[0]


def day18(inp):
    part1 = sum(parse_part1(line) for line in inp.splitlines())
    part2 = sum(parse_part2(line) for line in inp.splitlines())

    return part1, part2


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(day18(testinp))
    inp = open('day18.inp').read()
    print(day18(inp))
