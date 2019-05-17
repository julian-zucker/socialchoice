"""Functions that will add missing items into a partial ranking. All functions have the following signature:

Input is a (possibly) partial, but transitive win-graph, and a set of nodes to insert into that win-graph. The output is a
complete, fully connected, transitive win-graph."""
import random

import networkx as nx

import util
from ballot import PairwiseBallotBox


def place_randomly(win_graph, to_add):
    """Inserts each candidate to a random place in the ranking."""
    partial_ranking = _graph_to_ranking(win_graph)
    for item in to_add:
        partial_ranking.insert(random.randrange(0, len(partial_ranking) + 1), item)
    return _ranking_to_graph(partial_ranking)


def add_all_at_beginning(win_graph, to_add):
    """Adds all candidates as winning against everyone."""
    ranking = _graph_to_ranking(win_graph)
    ranking.insert(0, to_add)
    return _ranking_to_graph(ranking)


def add_all_at_end(win_graph, to_add):
    """Adds all candidates to the end of the ranking."""
    ranking = _graph_to_ranking(win_graph)
    ranking.append(to_add)
    return _ranking_to_graph(ranking)


def add_random_edges(win_graph, to_add):
    """Chooses a random pair of nodes that aren’t connected to each other, and then connects them, never adding
    edges that would result in a cycle, until the graph is a complete win-graph.
    """
    raise NotImplementedError


def add_edges_by_win_ratio(win_graph, to_add):
    """Adds edges into the win-graph in order of the win ratios of those matchups in the entire voting set,
    only adding edges that will not create cycles."""
    raise NotImplementedError


def _graph_to_ranking(g):
    return list(nx.topological_sort(g))


def _ranking_to_graph(r):
    return PairwiseBallotBox(util.ranking_to_pairwise_ballots(r)).get_victory_graph()
