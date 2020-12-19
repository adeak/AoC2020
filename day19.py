import re
import graphlib  # 3.9
from ast import literal_eval


def regexify(rules, sort_order, part2=False):
    """Turn a dict of rules into a huge regex for rule 0

    Since we're using the topological sort, we can readily forward replace everything.

    Special-case the regex for part 2:
        8: 42 | 42 8
            this is actually a (42)+ regex pattern
        11: 42 31 | 42 11 31
            this is a (42){n}(31){n} regex pattern with any n
            (we can probably only hard-code various cases using built-in re)
    """
    rules = rules.copy()  # make this re-entrant

    for index in sort_order:
        rule_raw = rules[index]  # to be replaced

        # unquote string literals
        if '"' in rule_raw:
            rules[index] = rule_raw.replace('"', '')
            continue

        if part2 and index == 8:
            rules[index] = f'({rules[42]})+'
        elif part2 and index == 11:
            # hack: use different number of equal repetitions
            patt1 = rules[42]
            patt2 = rules[31]
            new_rule = '|'.join(f'({patt1}){{{n}}}({patt2}){{{n}}}' for n in range(1, 10))
            rules[index] = f'({new_rule})'
        else:
            # replace every integer with the corresponding (guaranteed to be literal) pattern
            # preserve the pipe if there, but add enclosing parentheses
            rule_split = rule_raw.split()
            rule_replaced = ''.join([rules[int(dep)] if dep != '|' else '|' for dep in rule_split])
    
            if '|' in rule_replaced:
                rule_replaced = f'({rule_replaced})'
    
            rules[index] = rule_replaced

    # we only need to see if pattern 0 matches
    rex = re.compile(rules[0])

    return rex


def day19(inp, no_part_2=False):
    rules_block, messages = inp.split('\n\n')

    # parse rules into a dict first
    # also toposort the rules
    rules = {}
    toposorter = graphlib.TopologicalSorter()
    for rule in rules_block.splitlines():
        ind, rest = rule.split(': ')
        index = int(ind)
        rules[index] = rest

        # parse rules to pick out integer dependencies for building the dependency graph
        potential_dependencies = rest.replace('|', ' ').split()
        dependencies = [int(dep) for dep in potential_dependencies if dep.isdigit()]
        toposorter.add(index, *dependencies)

    sort_order = list(toposorter.static_order())

    # build a regex from the rules using the toposort order
    mega_regex = regexify(rules, sort_order)
    part1 = sum(1 for msg in messages.splitlines() if mega_regex.fullmatch(msg))

    if no_part_2:
        return part1

    # part 2: hack the regex during construction
    mega_regex_part2 = regexify(rules, sort_order, part2=True)
    part2 = sum(1 for msg in messages.splitlines() if mega_regex_part2.fullmatch(msg))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day19.testinp').read()
    print(day19(testinp, no_part_2=True))
    testinp2 = open('day19.testinp2').read()
    print(day19(testinp2)[1])
    inp = open('day19.inp').read()
    print(day19(inp))
