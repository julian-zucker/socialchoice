"""Functions that will create transitive win-graphs from (possibly) intransitive win-graphs.

Input is a intransitive win-graph, output is a transitive win-graph."""
import random
from functools import partial

import networkx as nx


def break_random_link(vote_set):
    """While there is a cycle, breaks the cycle by removing a random edge in it."""
    win_graph = nx.DiGraph()
    win_graph.add_edges_from((vote[0], vote[1]) for vote in vote_set)

    # Keep iterating until there are no cycles remaining
    while True:
        try:
            cycle = nx.find_cycle(win_graph)
            win_graph.remove_edge(*cycle[random.randrange(0, len(cycle))])
        except nx.NetworkXNoCycle:
            break

    assert nx.is_directed_acyclic_graph(win_graph)
    return win_graph


def make_break_weakest_link(edge_to_weight):
    """Given a mapping from edges to weights, resolves intransitivity by picking cycles at random, and removing
    the weakest edge in the chosen cycle. Eventually, there are no cycles left.

    :param edge_to_weight: a dictionary mapping (winner,loser) edges to weights (floats)
    :return: a transitive vote graph
    """
    # Partial function instead of local definition so that result can be pickled
    return partial(break_weakest_link, edge_to_weight)


def break_weakest_link(edge_to_weight, vote_set):
    """While there is a cycle, breaks the cycle by removing the weakest edge in it."""
    win_graph = nx.DiGraph()
    win_graph.add_edges_from((vote[0], vote[1]) for vote in vote_set)

    def weakest(edges):
        return min(edges, key=lambda e: edge_to_weight[e])

    # Keep iterating until there are no cycles remaining
    while True:
        try:
            cycle = nx.find_cycle(win_graph)
            win_graph.remove_edge(*weakest(cycle))
        except nx.NetworkXNoCycle:
            break

    assert nx.is_directed_acyclic_graph(win_graph)
    return win_graph


def make_add_edges_in_order(edge_to_weights):
    # Partial function instead of local definition so that result can be pickled
    return partial(add_edges_in_order, edge_to_weights)


def add_edges_in_order(edge_to_weights, vote_set):
    """Adds edges in order of weight, never adding edges that would create a cycle."""
    win_graph = nx.DiGraph()
    ordered_votes = sorted(vote_set, key=lambda e: edge_to_weights[(e[0], e[1])], reverse=True)
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
