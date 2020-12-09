def simulate(prog, part2=False):
    acc = 0
    ip = 0
    seen_instrs = {ip}
    while True:
        instr, arg = prog[ip]
        if instr == 'acc':
            offset = 1
            acc += arg
        elif instr == 'nop':
            offset = 1
        elif instr == 'jmp':
            offset = arg
        ip += offset

        if ip in seen_instrs:
            # part 1: we're done
            if not part2:
                return acc
            # part 2: need a new program
            return None

        seen_instrs.add(ip)

        if ip == len(prog):
            # part 2 finite execution, success
            return acc


def day08(inp):
    # parse into list of (op, arg) tuples
    prog = [((words := row.split())[0], int(words[1])) for row in inp.splitlines()]

    # part 1
    part1 = simulate(prog)

    # part 2
    swappables = [i for i,(op,_) in enumerate(prog) if op in {'jmp', 'nop'}]

    for i_swap in swappables:
        op, arg = prog[i_swap]
        op = 'jmp' if op == 'nop' else 'nop'
        prog_mutated = prog.copy()
        prog_mutated[i_swap] = op, arg

        if part2 := simulate(prog_mutated, part2=True):
            break

    return part1, part2


if __name__ == "__main__":
    testinp = open('day08.testinp').read()
    print(day08(testinp))
    inp = open('day08.inp').read()
    print(day08(inp))
