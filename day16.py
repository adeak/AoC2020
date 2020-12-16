from operator import itemgetter
from math import prod

def check_value(fields, value):
    """Check if a given value is valid for any field"""
    for intervals in fields.values():
        for interval in intervals:
            if value in interval:
                return True

    return False


def day16(inp, no_part_2=False):
    attrs, mine, rest = inp.strip().split('\n\n')

    # parse valid fields
    valid_fields = {}
    for attr_row in attrs.splitlines():
        name, tail = attr_row.split(': ')
        interval_texts = tail.split(' or ')
        intervals = [tuple(map(int, bounds.split('-'))) for bounds in interval_texts]
        ranges = [range(start, end + 1) for start, end in intervals]
        valid_fields[name] = ranges

    # parse my ticket
    my_values = list(map(int, mine.splitlines()[-1].split(',')))

    # part 1: find invalid tickets
    other_tickets = rest.splitlines()[1:]
    error_rate = 0
    tickets_keep = []  # list of parsed valid tickets
    for other_ticket in other_tickets:
        other_values = list(map(int, other_ticket.splitlines()[-1].split(',')))

        is_valid = True
        for value in other_values:
            if not check_value(valid_fields, value):
                error_rate += value
                is_valid = False

        if is_valid:
            tickets_keep.append(other_values)

    part1 = error_rate

    # part 2: find the order of fields by process of elimination
    #         (20! == 2432902008176640000 potential configurations)
    #
    #         but it's not that bad: n_fields * n_tickets is an upper bound on field/ticket checks
    #
    # to make it a bit faster: order potential fields by total interval length
    # start looking for the fields with shortest intervals

    interval_lengths = {name: sum(len(interval) for interval in intervals) for name, intervals in valid_fields.items()}

    sorted_keys = map(itemgetter(0), sorted(interval_lengths.items(), key=itemgetter(1)))
    sorted_fields = {k: valid_fields[k] for k in sorted_keys}  # python 3.7+

    field_order = {}  # field name -> index mapping
    while len(field_order) < len(valid_fields):
        for name, intervals in sorted_fields.items():
            if name in field_order:
                # skip already identified fields
                continue

            # skip already identified indices
            candidate_indices = set(range(len(my_values))) - set(field_order.values())
            for ticket in tickets_keep:
                for index, value in enumerate(ticket):
                    if index not in candidate_indices:
                        # nothing to check here
                        continue
                    if all(value not in interval for interval in intervals):
                        # this index is definitely out for this field
                        candidate_indices.remove(index)
                        continue
    
                if len(candidate_indices) == 1:
                    # we're the princes of the univeeerse
                    field_index = candidate_indices.pop()
                    field_order[name] = field_index
                    break

    if no_part_2:
        # skip final part 2 calculation for the test case
        print(f'field mapping: {field_order}')
        return part1

    part2 = prod(my_values[index] for field, index in field_order.items() if field.startswith('departur'))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    print(day16(testinp, no_part_2=True))
    inp = open('day16.inp').read()
    print(day16(inp))
