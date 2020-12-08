class Bag:
    def __init__(self, kind, children):
        self.kind = kind
        self.contents = children
        self.isin = set()
        self.bag_count = 1

def day07(inp):
    # parse the input into a dict of bags
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

    # post-processing
    for bag in bags.values():
        # replace children as string keys with children as bag keys
        bag.contents = {bags[k]: v for k, v in bag.contents.items()}

        # create reverse mapping
        for child in bag.contents:
            bags[child.kind].isin.add(bag)

    # part 1: find who might contain shiny gold (BFS)
    root = bags['shiny gold']
    to_visit = {root}
    unique_outermosts = set()
    while True:
        next_visit = set()
        for node in to_visit:
            unique_outermosts.add(node)
            next_visit |= bags[node.kind].isin

        # ignore already seen nodes
        to_visit = next_visit - unique_outermosts

        if not to_visit:
            break
    part1 = len(unique_outermosts) - 1 # ignore ourselves

    # part 2: sum up contents of shiny gold, start from leaves
    root.bag_count = 0  # don't count the root node, only contents
    leaves = {bag for bag in bags.values() if not bag.contents}
    remaining_bags = set(bags.values())
    while True:
        if root in leaves:
            part2 = root.bag_count
            break

        for leaf in leaves:
            for parent in leaf.isin:
                parent.bag_count += parent.contents[leaf] * leaf.bag_count
                del parent.contents[leaf]

        remaining_bags -= leaves
        leaves = {bag for bag in remaining_bags if not bag.contents}

    return part1, part2


if __name__ == "__main__":
    testinp = open('day07.testinp').read()
    print(day07(testinp))
    testinp2 = open('day07.testinp2').read()
    print(day07(testinp2)[1])
    inp = open('day07.inp').read()
    print(day07(inp))
