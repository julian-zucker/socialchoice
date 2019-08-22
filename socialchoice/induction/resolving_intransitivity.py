"""Functions that will create transitive win-graphs from (possibly) intransitive win-graphs.

Input is a intransitive win-graph, output is a transitive win-graph.

The easiest way to generate intransitivity resolvers is with the IntransitivityResolverFactory.
You construct it with the set of pairwise votes it will be resolving vote sets from, and then
can use its methods to generate intransitivity resolvers.
"""
import random
from functools import partial

import networkx as nx

from socialchoice import BallotBox, PairwiseBallotBox


class IntransitivityResolverFactory:
    def __init__(self, ballot_box: BallotBox):
        self.pairwise_ballots = ballot_box
        wg = ballot_box.get_matchup_graph()
        self.edge_to_win_ratio = {e: wg.get_edge_data(*e)["margin"] for e in wg.edges}

    def make_break_random_link(self):
        return partial(break_random_link)

    def make_break_weakest_link(self):
        return make_break_weakest_link(self.edge_to_win_ratio)

    def make_add_edges_in_order(self):
        return make_add_edges_in_order(self.edge_to_win_ratio)


def break_random_link(vote_set):
    """While there is a cycle, breaks the cycle by removing a random edge in it."""
    win_graph = PairwiseBallotBox(vote_set).get_victory_graph()

    # Keep iterating until there are no cycles remaining
    while True:
        try:
            cycle = nx.find_cycle(win_graph)
            win_graph.remove_edge(*cycle[random.randrange(0, len(cycle))])
        except nx.NetworkXNoCycle:
            break

    assert nx.is_directed_acyclic_graph(win_graph)
    return win_graph


def make_break_weakest_link(edge_to_win_ratio):
    """Given a mapping from edges to weights, resolves intransitivity by picking cycles at random, and removing
    the weakest edge in the chosen cycle. Eventually, there are no cycles left.

    :param edge_to_win_ratio: a dictionary mapping (winner,loser) edges to weights (floats)
    :return: a transitive vote graph
    """
    # Partial function instead of local definition so that result can be pickled
    func = partial(break_weakest_link, edge_to_win_ratio)
    return func


def break_weakest_link(edge_to_win_ratio, vote_set):
    """While there is a cycle, breaks the cycle by removing the weakest edge in it."""
    win_graph = PairwiseBallotBox(vote_set).get_victory_graph()

    def weakest(edges):
        return min(edges, key=lambda e: edge_to_win_ratio[e])

    # Keep iterating until there are no cycles remaining
    while True:
        try:
            cycle = nx.find_cycle(win_graph)
            win_graph.remove_edge(*weakest(cycle))
        except nx.NetworkXNoCycle:
            break

    assert nx.is_directed_acyclic_graph(win_graph)
    return win_graph


def make_add_edges_in_order(edge_to_win_ratio):
    # Partial function instead of local definition so that result can be pickled
    func = partial(add_edges_in_order, edge_to_win_ratio)
    return func


def add_edges_in_order(edge_to_win_ratio, vote_set):
    """Adds edges in order of weight, never adding edges that would create a cycle."""
    win_graph = nx.DiGraph()
    ordered_votes = sorted(vote_set, key=lambda e: edge_to_win_ratio[(e[0], e[1])], reverse=True)

    for c1, c2, result in ordered_votes:
        try:
            win_graph.add_edge(c1, c2)
            cycles = nx.find_cycle(win_graph)
            # If we hit this line, a NoCycle exception was not thrown, therefore there is a cycle and we have to
            # remove an edge from it
            win_graph.remove_edge(c1, c2)
        except nx.NetworkXNoCycle:
            continue

    assert nx.is_directed_acyclic_graph(win_graph)
    return win_graph
