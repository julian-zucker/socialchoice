from itertools import combinations


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


def ranking_with_all_sets(r):
    out = []
    for item in r:
        if isinstance(item, set):
            out.append(item)
        else:
            out.append({item})
    return out


def ranking_to_pairwise_ballots(ranking):
    ranking = ranking_with_all_sets(ranking)
    # to convert to pairwise ballots, we'll have to look at each ranking
    pairwise_ballots = []
    # and within each set in that ranking, all pairs of elements (combinations of size 2) are tied
    for candidate_set in ranking:
        for candidate1, candidate2 in combinations(candidate_set, 2):
            pairwise_ballots.append((candidate1, candidate2, "tie"))

    # For each candidate set, and every candidate set after them in the ranking, the first set wins against
    # each set in the second
    for i, winner_candidate_set in enumerate(ranking):
        for losing_candidate_set in ranking[i + 1:]:
            # (but because they are both sets, we have to iterate over each candidate in each)
            for winning_candidate in winner_candidate_set:
                for losing_candidate in losing_candidate_set:
                    pairwise_ballots.append((winning_candidate, losing_candidate, "win"))

    return pairwise_ballots
