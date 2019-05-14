"""
Collapse pairwise votes into ranked choice votes.

This task can be conceptually split into two: resolving intransitivity, and assuming the values of un-voted-on items.
"""

import random
import networkx as nx
from more_itertools import flatten


def pairwise_collapse_by_voter(pairwise_votes_by_voter, candidates=None, upsample=False):
    """Given a list of lists of pairwise votes, where each list corresponds to one voter's complete vote set,
    produces a list of rankings over the candidates.

    :param pairwise_votes_by_voter: the votes, as a list of vote sets from a voter.
    :param candidates: the list of candidates, inferred from the pairwise votes if not provided. Recommended to provide
    for small vote sets if worried about not all candidates appearing at least once in the votes.
    :param upsample: whether to put in one ranking per voter (False) or one ranking per pairwise vote (True)
    :return:
    """
    candidates = candidates or set(flatten((vote[0], vote[1]) for vote in flatten(pairwise_votes_by_voter)))

    rankings = []

    for voter in pairwise_votes_by_voter:
        if upsample:
            # Once per pairwise vote
            for _ in voter:
                rankings.append(pairwise_collapse(voter, candidates))
        else:
            # Once per voter
            rankings.append(pairwise_collapse(voter, candidates))

    return rankings

def pairwise_collapse(pairwise_votes, candidates=None) -> list:
    """Converts a set of pairwise votes into a ranking over all of the candidates."""
    candidates = candidates or set(flatten([(v[0], v[1]) for v in pairwise_votes]))
    transitive_votes = resolve_intransitivity(pairwise_votes)
    complete_ranking = insert_unvoted_items(transitive_votes, candidates)
    return complete_ranking


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

        # Create a DAG, only add edges that won't create a cycle.
        transitive_votes.add_edge(c1, c2)
        while True:
            try:
                cycles = nx.find_cycle(transitive_votes)
                # Remove it if we could find a cycle
                transitive_votes.remove_edge(*cycles[random.randint(0, len(cycles)-1)])
            except nx.NetworkXNoCycle:
                break

    # If it's not a DAG, something's gone horribly wrong above, and also we won't be able to toposort.
    assert nx.is_directed_acyclic_graph(transitive_votes)
    return list(nx.topological_sort(transitive_votes))


def insert_unvoted_items(partial_ranking, candidates):
    """Adds each missing candidate to a random place in the partial ranking
    (but not the first or last place, if we can avoid it. This method is relatively simple.

    TODO add more sophisticated (elo-based, or otherwise normally distributed) method for missing candidate insertion
    """
    not_added = candidates.difference(partial_ranking)

    for elem in not_added:
        insertion_index = random.randint(1, max(1, len(partial_ranking)-1))
        partial_ranking.insert(insertion_index, elem)

    return partial_ranking
