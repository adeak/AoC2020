class Bag:
    def __init__(self, kind, children):
        self.kind = kind
        self.contains = children
        self.isin = set()

class Node:
    def __init__(self, kind, parent, count):
        self.kind = kind
        self.parent = parent
        self.count = count
        self.children = set()

def day07(inp):
    bags = {}
    for line in inp.splitlines():
        kind, tail = line.split(' bags contain ')
        children = {}
        if not tail.startswith('no other'):
            tail_split = tail.split(',')
            for child in tail_split:
                words = child.split()
                count = int(words[0])
                child_kind = ' '.join(words[1:3])
                children[child_kind] = count
        bags[kind] = Bag(kind, children)

    # create reverse mapping
    for kind, bag in bags.items():
        # kind contains bag.contains
        for child_kind in bag.contains:
            bags[child_kind].isin.add(kind)

    # part 1: find who might contain
    root = 'shiny gold'
    to_visit = {root}
    unique_outermosts = set()
    while True:
        next_visit = set()
        for node in to_visit:
            unique_outermosts.add(node)
            next_visit |= bags[node].isin

        # ignore already seen nodes
        to_visit = next_visit - unique_outermosts

        if not to_visit:
            break

    part1 = len(unique_outermosts) - 1 # ignore our own

    # part 2: walk contents
    root = Node('shiny gold', parent=None, count=1)
    to_visit = {root}
    # also expect multiple hits of the same bag kind

    leaves = set()
    tot = 0
    while True:
        next_visit = set()
        for node in to_visit:
            # check for children
            children = bags[node.kind].contains.items()
            if not children:
                leaves.add(node)
                continue

            for child_kind, cnt in children:
                child_node = Node(child_kind, parent=node, count=node.count * cnt)
                tot += child_node.count
                node.children.add(child_node)
                next_visit.add(child_node)

        to_visit = next_visit
        if not to_visit:
            break

    part2 = tot

    return part1, part2


if __name__ == "__main__":
    testinp = open('day07.testinp').read()
    print(day07(testinp))
    testinp2 = open('day07.testinp2').read()
    print(day07(testinp2)[1])
    inp = open('day07.inp').read()
    print(day07(inp))
