from collections import deque
from itertools import islice

def play_combat(decks, part1=True):
    """Play recursive combat... recursively.

    Return the winner index and the winning deck
    """
    history = set()
    while all(decks):
        # if a configuration was already seen: game over, player 1 wins
        # (irrelevant for part 1)
        configuration = tuple(map(tuple, decks))
        if configuration in history:
            return 0, decks[0]
        history.add(configuration)

        # draw as normal
        nums = num1, num2 = [deck.popleft() for deck in decks]

        if part1 or num1 > len(decks[0]) or num2 > len(decks[1]):
            # we can't recurse, round over
            # (or part 1 where we never recurse)
            winner_index = 0 if num1 > num2 else 1
        else:
            # we recurse; copy the deck slices
            subdecks = [deque(list(islice(deck, num))) for num, deck in zip(nums, decks)]
            winner_index, _ = play_combat(subdecks)

        # winner index gets the cards with winner index card first (to the left)
        target = decks[winner_index]
        nums = nums[winner_index], nums[1 - winner_index]

        target.extend(nums)

    # find the winner index: who has cards left
    winner_index = 0 if decks[0] else 1

    return winner_index, decks[winner_index]


def day22_recursive(inp):
    # parse cards into deques; left end of the deque is the top of the deck
    blocks = inp.split('\n\n')
    decks = [deque(map(int, block.splitlines()[1:])) for block in blocks]

    # use recursion for part 2 even if it's evil

    answers = []
    for part1 in True, False:
        _, winning_deck = play_combat([deck.copy() for deck in decks], part1)
        res = sum(i*val for i, val in enumerate(reversed(winning_deck), start=1))
        answers.append(res)

    return tuple(answers)


# ^^^ above recursive
#
# vvv below iterative


def day22(inp, part1=True):
    # parse cards into deques; left end of the deque is the top of the deck
    blocks = inp.split('\n\n')
    decks = [deque(map(int, block.splitlines()[1:])) for block in blocks]

    # avoid recursion out of spite
    multidecks = [decks]
    history = set(map(tuple, decks))
    histories = [history]
    suspended_draws = []
    
    # run until outermost game is over
    while len(multidecks) > 1 or all(multidecks[0]):
        # check deck history for infinite loops
        # (irrelevant for part 1)
        configuration = tuple(map(tuple, decks))
        if not all(decks) or configuration in history:
            # this game is over
            if configuration in history:
                winner_index = 0
            else:
                winner_index = 0 if decks[0] else 1
            multidecks.pop()
            histories.pop()
            decks = multidecks[-1]
            history = histories[-1]
            nums = suspended_draws.pop()
        else:
            # draw as normal
            nums = num1, num2 = [deck.popleft() for deck in decks]

            if part1 or num1 > len(decks[0]) or num2 > len(decks[1]):
                # we can't recurse, round over
                # (or part 1 where we never recurse)
                winner_index = 0 if num1 > num2 else 1
            else:
                # we recurse; copy the deck slices
                decks = [deque(list(islice(deck, num))) for num, deck in zip(nums, decks)]
                multidecks.append(decks)
                history = set()
                histories.append(history)
                suspended_draws.append(nums)
                continue
            history.add(configuration)

        # winner index gets the cards with winner index card first (to the left)
        # winner may have been determined in one level deeper
        target = decks[winner_index]
        nums = nums[winner_index], nums[1 - winner_index]

        target.extend(nums)

    winning_deck = decks[0] or decks[1]
    res = sum(i*val for i, val in enumerate(reversed(winning_deck), start=1))

    return res


if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    # print(day22_recursive(testinp))
    print(day22(testinp))
    print(day22(testinp, part1=False))
    inp = open('day22.inp').read()
    # print(day22_recursive(inp))
    print(day22(inp))
    print(day22(inp, part1=False))
