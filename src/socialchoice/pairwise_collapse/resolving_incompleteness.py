"""Functions that will add missing items into a partial ranking. All functions have the following signature:

Input is a (possibly) partial, but transitive win-graph, and a set of nodes to insert into that win-graph. The output is a
complete, fully connected, transitive win-graph."""
import random

import networkx as nx


def place_randomly(win_graph, to_add):
    """Inserts each candidate to a random place in the ranking."""
    partial_ranking = list(nx.topological_sort(win_graph))
    for item in to_add:
        partial_ranking.insert(item, random.randint(0, max(1, len(partial_ranking) - 1)))
    return partial_ranking

def add_all_at_beginning(win_graph, to_add):
    """Adds all candidates as winning against everyone."""
    pass

def add_all_at_end(win_graph, to_add):
    """Adds all candidates to the end of the ranking."""
    pass

def add_random_edges(win_graph, to_add):
    """Chooses a random pair of nodes that aren’t connected to each other, and then connects them, never adding
    edges that would result in a cycle, until the graph is a complete win-graph.
    """
    pass

def add_edges_by_win_ratio(win_graph, to_add):
    """Adds edges into the win-graph in order of the win ratios of those matchups in the entire voting set,
    only adding edges that will not create cycles."""
    pass

