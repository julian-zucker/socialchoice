
def num_inversions(ranking1, ranking2):
    """This is a measure of how far apart two rankings are, by the number of inversions. An inversion is a
    swapping of two elements, so [1,2,3] and [1,3,2] have one inversion, while [1,2,3] and [3,1,2] have two.

    :raises ValueError: if called with rankings that don't contain the same elements.
    """
    # So that we can accept iterables of any type - store all contents in list because we go over them multiple times
    ranking1 = list(ranking1)
    ranking2 = list(ranking2)

    if set(ranking1) != set(ranking2):
        raise ValueError(f"Rankings must contain same elements, {ranking1} and {ranking2} differ")

    inversions = 0
    for index, item1 in enumerate(ranking1):
        for item2 in ranking1[index + 1:]:
            if ranking2.index(item1) >= ranking2.index(item2):
                inversions += 1

    return inversions
