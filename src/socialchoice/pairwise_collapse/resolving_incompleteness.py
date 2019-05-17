"""Functions that will add missing items into a partial ranking. All functions have the following signature:

Input is a (possibly) partial, but transitive win-graph, and a set of nodes to insert into that win-graph. The output is a
complete, fully connected, transitive win-graph."""
import random

import networkx as nx
from more_itertools import flatten

import util
from ballot import PairwiseBallotBox


def place_randomly(win_graph: nx.DiGraph, to_add: set) -> nx.DiGraph:
    """Inserts each candidate to a random place in the ranking."""
    partial_ranking = _graph_to_ranking(win_graph)
    for item in to_add:
        partial_ranking.insert(random.randrange(0, len(partial_ranking) + 1), item)
    return _ranking_to_graph(partial_ranking)


def add_all_at_beginning(win_graph: nx.DiGraph, to_add: set) -> nx.DiGraph:
    """Adds all candidates as winning against everyone."""
    ranking = _graph_to_ranking(win_graph)
    ranking.insert(0, to_add)
    return _ranking_to_graph(ranking)


def add_all_at_end(win_graph: nx.DiGraph, to_add: set) -> nx.DiGraph:
    """Adds all candidates to the end of the ranking."""
    ranking = _graph_to_ranking(win_graph)
    ranking.append(to_add)
    return _ranking_to_graph(ranking)


def add_random_edges(win_graph: nx.DiGraph, to_add: set) -> nx.DiGraph:
    """Chooses a random pair of nodes that aren’t connected to each other, and then connects them, never adding
    edges that would result in a cycle, until the graph is a complete win-graph.
    """
    win_graph = win_graph.copy()
    candidates = set(win_graph.nodes).union(to_add)
    edge_list = []
    for u in candidates:
        for v in candidates:
            if u != v:
                edge_list.append((u, v))

    random.shuffle(edge_list)

    # Existing edges don't have to be checked
    for edge in win_graph.edges:
        edge_list.remove(edge)

    for c1, c2 in edge_list:
        try:
            win_graph.add_edge(c1, c2)
            nx.find_cycle(win_graph)
            win_graph.remove_edge(c1, c2)
        except nx.NetworkXNoCycle:
            pass

    return win_graph


def make_add_edges_by_win_ratio(edges_by_win_ratio):
    """Given a list of edges by win ratio, creates a function that will resolve incompleteness by adding
    non-cycle-creating edges from the list until the graph is complete.

    :param edges_by_win_ratio: the list of edges as 2-tuples of (winner, loser), ordered by win rate, highest first
    :return:
    """

    def add_edges_by_win_ratio(win_graph: nx.DiGraph, to_add: set) -> nx.DiGraph:
        """Adds edges into the win-graph in order of the win ratios of those matchups in the entire voting set,
        only adding edges that will not create cycles."""
        for (c1, c2) in edges_by_win_ratio:
            try:
                win_graph.add_edge(c1, c2)
                nx.find_cycle(win_graph)
                win_graph.remove_edge(c1, c2)
            except nx.NetworkXNoCycle:
                pass

        assert all(candidate in win_graph.nodes for candidate in to_add)
        return win_graph

    return add_edges_by_win_ratio


def _graph_to_ranking(g: nx.DiGraph) -> list:
    return list(nx.topological_sort(g))


def _ranking_to_graph(r: list) -> nx.DiGraph:
    return PairwiseBallotBox(util.ranking_to_pairwise_ballots(r)).get_victory_graph()
