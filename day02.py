def valid_pwd(policy, pwd, part2=False):
    char, (at_least, at_most) = policy.copy().popitem()
    if not part2:
        return at_least <= pwd.count(char) <= at_most
    is_valid = (pwd[at_least - 1] == char) ^ (pwd[at_most - 1] == char)
    return is_valid

def day02(inp):
    datarows = []
    for row in inp.splitlines():
        policypart, pwd = row.split(': ')
        fromto, char = policypart.split()
        at_least, at_most = map(int, fromto.split('-'))
        policy = {char: (at_least, at_most)}
        datarows.append((policy, pwd))
    
    # count valids
    part1 = sum(1 for policy, pwd in datarows if valid_pwd(policy, pwd))
    part2 = sum(1 for policy, pwd in datarows if valid_pwd(policy, pwd, part2=True))

    return part1, part2

if __name__ == "__main__":
    inp = open('day02.inp').read()
    print(day02(inp))
