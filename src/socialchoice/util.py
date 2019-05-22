from itertools import combinations


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
        for losing_candidate_set in ranking[i + 1 :]:
            # (but because they are both sets, we have to iterate over each candidate in each)
            for winning_candidate in winner_candidate_set:
                for losing_candidate in losing_candidate_set:
                    pairwise_ballots.append((winning_candidate, losing_candidate, "win"))

    return pairwise_ballots


def candidates_in_ranked_choice_ballot(ballot):
    candidate_set = set()
    for item in ballot:
        if isinstance(item, set):
            # If there is a set, it is a tie, so process it one element at a time.
            for elem in item:
                if elem in candidate_set:
                    raise ValueError(f"Candidate {elem} appears multiple times in {ballot}")
                candidate_set.add(elem)
        else:
            # If it's not a set, we can just process one at a time.
            if item in candidate_set:
                raise ValueError(f"Candidate {item} appears multiple times in {ballot}")
            candidate_set.add(item)
    return candidate_set
