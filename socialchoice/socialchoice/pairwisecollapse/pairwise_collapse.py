"""
Collapse pairwise votes into ranked choice votes.
"""


def pairwise_collapse(
    pairwise_votes, candidates, intransitivity_resolver, incompleteness_resolver
) -> list:
    """
    Converts a set of pairwise votes into a ranking over all of the candidates.

    :param pairwise_votes: The pairwise votes, as a list of 2-tuples
    :param candidates: The list of candidates in the elections
    :param intransitivity_resolver: function used to resolve intransitivity
    :param incompleteness_resolver: function used to complete the transitive sub-graph
    """
    transitive_votes = intransitivity_resolver(pairwise_votes)
    return incompleteness_resolver(transitive_votes, candidates)
