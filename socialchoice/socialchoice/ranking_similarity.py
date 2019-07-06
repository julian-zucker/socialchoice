import scipy.stats


def kendalls_tau(ordering1, ordering2):
    """
    :return: The kendall tau coefficient between these two orderings.
    """

    def ranks_of_candidates(ranking):
        """
        :param ranking: An ordering over candidates.
        :return: The ranks of each candidate in the specified ordering.

        >>> ranks_of_candidates([1, 3, 2])
        {1: 0, 3: 1, 2: 2}
        """
        # A mapping from each candidate to their rank.
        candidate_to_rank = {}
        current_rank = 0

        for tie_set in ranking:
            if isinstance(tie_set, set):
                # If there's a set, then each candidate get's placed at the middle: so divide
                # the length of the set by two, and assign that rank to each candidate.
                current_rank += len(tie_set) / 2
                for candidate in tie_set:
                    candidate_to_rank[candidate] = current_rank
                current_rank += len(tie_set) / 2
            else:
                # Otherwise, we only have one, so add one and assign that rank.
                candidate = tie_set
                current_rank += 1
                candidate_to_rank[candidate] = current_rank
        return candidate_to_rank

    ranks1 = ranks_of_candidates(ordering1)
    ranks2 = ranks_of_candidates(ordering2)

    x = [ranks1[item] for item in ordering1]
    y = [ranks2[item] for item in ordering1]
    correlation, pvalue = scipy.stats.kendalltau(x, y)
    return correlation
