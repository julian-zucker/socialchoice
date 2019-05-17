"""
Collapse pairwise votes into ranked choice votes.

This task can be conceptually split into two: resolving intransitivity, and assuming the values of un-voted-on items.
"""

import random
import networkx as nx
from more_itertools import flatten



def pairwise_collapse_by_voter(pairwise_votes_by_voter,
                               candidates,
                               upsample,
                               intransitivity_resolver,
                               incompleteness_resolver):
    """Given a list of lists of pairwise votes, where each list corresponds to one voter's complete vote set,
    produces a list of rankings over the candidates.

    :param pairwise_votes_by_voter: the votes, as a list of vote sets from a voter.
    :param candidates: the list of candidates, inferred from the pairwise votes if not provided. Recommended to provide
    for small vote sets if worried about not all candidates appearing at least once in the votes.
    :param upsample: whether to put in one ranking per voter (False) or one ranking per pairwise vote (True)
    :param intransitivity_resolver: the function to be used to resolve intransitivites
    :param incompleteness_resolver: the function to be used to resolve incompleteness
    :return:
    """
    candidates = candidates or set(flatten((vote[0], vote[1]) for vote in flatten(pairwise_votes_by_voter)))

    rankings = []

    for voter_votes in pairwise_votes_by_voter:
        if upsample:
            rankings += pairwise_collapse_upsampling(voter_votes, candidates, intransitivity_resolver, incompleteness_resolver)
        else:
            rankings.append(pairwise_collapse(voter_votes, candidates, intransitivity_resolver, incompleteness_resolver))

    return rankings


def pairwise_collapse(pairwise_votes, candidates, intransitivity_resolver, incompleteness_resolver) -> list:
    """Converts a set of pairwise votes into a ranking or list of rankings over all of the candidates.
    Returns a single ranking if `upsample` is falsy, and a list of rankings with length `len(pairwise_votes)
    if `upsample` is truthy. """
    transitive_votes = intransitivity_resolver(pairwise_votes)
    return insert_unvoted_items(incompleteness_resolver, transitive_votes, candidates)


def pairwise_collapse_upsampling(pairwise_votes, candidates, intransitivity_resolver, incompleteness_resolver):
    transitive_votes = [intransitivity_resolver(pairwise_votes)] * len(pairwise_votes)
    return [insert_unvoted_items(incompleteness_resolver, v, candidates) for v in transitive_votes]


def insert_unvoted_items(insertion_scheme, partial_ranking, candidates):
    not_added = candidates.difference(partial_ranking)
    return insertion_scheme(partial_ranking, not_added)
