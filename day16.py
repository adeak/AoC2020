from operator import itemgetter  # only for naive version
from math import prod  # only for naive version

import numpy as np

def check_value(fields, value):
    """Check if a given value is valid for any field

    (unused for numpy version)
    """
    for intervals in fields.values():
        for interval in intervals:
            if value in interval:
                return True

    return False


def day16_naive(inp, no_part_2=False):
    """Original, native python version"""
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


def day16(inp, no_part_2=False):
    """Numpy version; 100x faster, and obviously cooler"""
    attrs, mine, rest = inp.strip().split('\n\n')

    # parse valid fields
    valid_fields = {}
    for attr_row in attrs.splitlines():
        name, tail = attr_row.split(': ')
        interval_texts = tail.split(' or ')
        intervals = [tuple(map(int, bounds.split('-'))) for bounds in interval_texts]
        valid_fields[name] = intervals

    # parse my ticket
    my_values = np.fromstring(mine.splitlines()[-1], sep=',', dtype=int)

    # parse other tickets
    other_tickets = rest.splitlines()[1:]
    num_tickets = len(other_tickets)
    ticket_arr = np.fromstring(','.join(other_tickets), sep=',', dtype=int).reshape(num_tickets, -1)

    # part 1: find invalid tickets
    invalid_mask = ~np.logical_or.reduce([(interval[0] <= ticket_arr) & (ticket_arr <= interval[1]) for intervals in valid_fields.values() for interval in intervals])
    part1 = ticket_arr[invalid_mask].sum()

    # discard invalid tickets
    ticket_arr = ticket_arr[~invalid_mask.any(axis=1)]

    # compare every field to every interval
    matching_masks = np.array([[(interval[0] <= ticket_arr) & (ticket_arr <= interval[1])
                                   for interval in intervals]
                                for intervals in valid_fields.values()])  # shape (n_fields, 2, n_tickets, n_fields)
    potential_matches = np.logical_and.reduce(np.logical_or.reduce(matching_masks, axis=1), axis=1)  # shape (n_fields, n_fields)

    # potential_matches is True at (i, j) if field i of the header can be at index j

    matching_field_num = potential_matches.sum(-1)
    constraint_order = matching_field_num.argsort()
    name_order = np.array([*valid_fields])[constraint_order]
    potential_matches[...] = potential_matches[constraint_order, :]

    # constraint_order is in which we can unravel the knot
    # because there's only a unique solution if the number of potential indices
    # for each potential field are a permutation of range(n_fields)
    #
    # so we can go starting from the single-candidate field, and keep excluding
    # one field after the other

    if no_part_2:
        print(f'test input field order: {name_order.tolist()}')
        return part1

    # there might be a smarter way to do this:
    departure_indices = []
    for i, (name, matches) in enumerate(zip(name_order, potential_matches)):
        matched_index = matches.nonzero()[0][0]
        if name.startswith('departure'):
            departure_indices.append(matched_index)
        potential_matches[:, matched_index] = False

    part2 = my_values[departure_indices].prod()

    return part1, part2


if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    #print(day16_naive(testinp, no_part_2=True))
    print(day16(testinp, no_part_2=True))
    inp = open('day16.inp').read()
    #print(day16_naive(inp))
    print(day16(inp))
