"""
Collapse pairwise votes into ranked choice votes.

This task can be conceptually split into two: resolving intransitivity, and assuming the values of un-voted-on items.
This problem is deeply underspecified, see the tests for an honest spec.
"""

import random
import networkx as nx
from more_itertools import flatten


def pairwise_collapse(pairwise_votes, candidates=None) -> list:
    candidates = candidates or set(flatten([(v[0], v[1]) for v in pairwise_votes]))


    transitive_votes = resolve_intransitivity(pairwise_votes)
    complete_ranking = insert_unvoted_items(transitive_votes, candidates)
    return complete_ranking


def resolve_intransitivity(pairwise_votes):
    """Resolves any intransitivities in a set of votes.

    :param pairwise_votes: a set of votes from one user, as an iterable of vote-tuples
    :return: a set of transitive preferences, as an array of two-tuples like `(winner, loser)`
    """

    transitive_votes = nx.DiGraph()

    shuffled_votes = random.sample(pairwise_votes, len(pairwise_votes))
    for c1, c2, result in shuffled_votes:
        if result == "tie":
            continue

        if result == "loss":
            c1, c2 = c2, c1

        transitive_votes.add_edge(c1, c2)
        try:
            nx.find_cycle(transitive_votes)
            # Remove it if we could find a cycle
            transitive_votes.remove_edge(c1, c2)
        except nx.NetworkXNoCycle:
            pass

    assert nx.is_directed_acyclic_graph(transitive_votes)
    return list(nx.topological_sort(transitive_votes))


def insert_unvoted_items(partial_ranking, candidates):
    not_added = candidates.difference(partial_ranking)

    for elem in not_added:
        insertion_index = random.randint(1, max(1, len(partial_ranking)-1))
        partial_ranking.insert(insertion_index, elem)

    return partial_ranking
