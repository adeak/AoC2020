def day21(inp):
    all_ingredients = []
    all_allergens = []
    potential_ingredients = {}  # allergen -> ingredients
    for line in inp.splitlines():
        ingredient_list, allergen_list = line[:-1].split(' (contains ')
        ingredients = set(ingredient_list.split())
        allergens = set(allergen_list.split(', '))
        all_ingredients.append(ingredients)
        all_allergens.append(allergens)
        
        for allergen in allergens:
            if allergen not in potential_ingredients:
                potential_ingredients[allergen] = ingredients.copy()
            else:
                potential_ingredients[allergen] &= ingredients

    # for each food find the overlap in ingredients and overlap in allergens
    # if there's only one overlapping ingredient and allergen, we can pinpoint one
    # -> remove from the remaining potential ingredients -> repeat
    # in the end we must end up with 1 potential ingredient for every allergen

    known_allergens = set()
    while True:
        # eliminate those that are uniquely known
        new_known_allergens = {allergen for allergen, ingredients in potential_ingredients.items()
                               if allergen not in known_allergens and len(ingredients) == 1}
        new_known_ingredients = {ingredient for allergen in new_known_allergens
                                 for ingredient in potential_ingredients[allergen]}

        if not new_known_allergens:
            # we've converged
            break

        # remove these from the potential lists
        for allergen in potential_ingredients.keys() - new_known_allergens:
            potential_ingredients[allergen] -= new_known_ingredients

        known_allergens |= new_known_allergens

    part1 = sum(1 for ingredients in all_ingredients for ingredient in ingredients
                if all(ingredient not in pot_ingredients
                           for pot_ingredients in potential_ingredients.values()))
    part2 = ','.join(next(iter(ingredients)) for allergens, ingredients in sorted(potential_ingredients.items()))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day21.testinp').read()
    print(day21(testinp))
    inp = open('day21.inp').read()
    print(day21(inp))
