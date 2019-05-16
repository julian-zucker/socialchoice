"""
Collapse pairwise votes into ranked choice votes.

This task can be conceptually split into two: resolving intransitivity, and assuming the values of un-voted-on items.
"""

import random
import networkx as nx
from more_itertools import flatten

from ranking_completion_schemes import fill_uniformly


def pairwise_collapse_by_voter(pairwise_votes_by_voter,
                               candidates=None,
                               upsample=False,
                               ranking_completion_scheme=fill_uniformly):
    """Given a list of lists of pairwise votes, where each list corresponds to one voter's complete vote set,
    produces a list of rankings over the candidates.

    :param pairwise_votes_by_voter: the votes, as a list of vote sets from a voter.
    :param candidates: the list of candidates, inferred from the pairwise votes if not provided. Recommended to provide
    for small vote sets if worried about not all candidates appearing at least once in the votes.
    :param upsample: whether to put in one ranking per voter (False) or one ranking per pairwise vote (True)
    :param ranking_completion_scheme: one of "uniform", "elo", "bayesian": see
    :return:
    """
    candidates = candidates or set(flatten((vote[0], vote[1]) for vote in flatten(pairwise_votes_by_voter)))

    rankings = []

    for voter_votes in pairwise_votes_by_voter:
        if upsample:
            rankings += pairwise_collapse_upsampling(voter_votes, candidates, ranking_completion_scheme)
        else:
            rankings.append(pairwise_collapse(voter_votes, candidates, ranking_completion_scheme))

    return rankings


def pairwise_collapse(pairwise_votes, candidates=None, ranking_completion_scheme=fill_uniformly) -> list:
    """Converts a set of pairwise votes into a ranking or list of rankings over all of the candidates.
    Returns a single ranking if `upsample` is falsy, and a list of rankings with length `len(pairwise_votes)
    if `upsample` is truthy. """
    candidates = candidates or set(flatten([(v[0], v[1]) for v in pairwise_votes]))
    transitive_votes = resolve_intransitivity(pairwise_votes)
    return insert_unvoted_items(ranking_completion_scheme, transitive_votes, candidates)


def pairwise_collapse_upsampling(pairwise_votes, candidates=None, ranking_completion_scheme=fill_uniformly):
    candidates = candidates or set(flatten([(v[0], v[1]) for v in pairwise_votes]))
    transitive_votes = [resolve_intransitivity(pairwise_votes)] * len(pairwise_votes)
    return [insert_unvoted_items(ranking_completion_scheme, v, candidates) for v in transitive_votes]


def resolve_intransitivity(pairwise_votes):
    """Resolves any intransitivities in a set of votes.

    :param pairwise_votes: a set of votes from one user, as an iterable of vote-tuples
    :return: a list containing a (possibly partial) ranking over the candidates mentioned in "win" or "loss" pairs
    """
    transitive_votes = nx.DiGraph()

    shuffled_votes = random.sample(pairwise_votes, len(pairwise_votes))
    for c1, c2, result in shuffled_votes:
        # For now, ignore ties. This probably could be improved - ties do give us information
        if result == "tie":
            continue

        # Ensure that c1 is the victor and c2 the loser, by swapping if they are a loss
        if result == "loss":
            c1, c2 = c2, c1

        transitive_votes.add_edge(c1, c2)

    # convert to DAG by removing edges from every cycle
    while True:
        try:
            cycles = nx.find_cycle(transitive_votes)
            # If we hit this line, a NoCycle exception was not thrown, therefore there is a cycle and we have to
            # remove an edge from it
            transitive_votes.remove_edge(*cycles[random.randint(0, len(cycles) - 1)])
        except nx.NetworkXNoCycle:
            break

    # If it's not a DAG, something's gone horribly wrong above, and also we won't be able to toposort.
    assert nx.is_directed_acyclic_graph(transitive_votes)
    return list(nx.topological_sort(transitive_votes))


def insert_unvoted_items(insertion_scheme, partial_ranking, candidates):
    not_added = candidates.difference(partial_ranking)
    return insertion_scheme(partial_ranking, not_added)
