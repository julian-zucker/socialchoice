"""Functions that will create transitive win-graphs from (possibly) intransitive win-graphs.

Input is a intransitive win-graph, output is a transitive win-graph."""
import random

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


def break_weakest_link(vote_set):
    """While there is a cycle, breaks the cycle by removing the weakest edge in it."""
    win_graph = nx.DiGraph()
    win_graph.add_edges_from((vote[0], vote[1]) for vote in vote_set)

    def weakest(edges):
        raise NotImplementedError("TODO implement me")

    # Keep iterating until there are no cycles remaining
    while True:
        try:
            cycle = nx.find_cycle(win_graph)
            win_graph.remove_edge(*weakest(cycle[random.randrange(0, len(cycle))]))
        except nx.NetworkXNoCycle:
            break

    assert nx.is_directed_acyclic_graph(win_graph)
    return win_graph


def add_edges_in_order(vote_set):
    """Resolves any intransitivities in a set of votes."""
    win_graph = nx.DiGraph()

    shuffled_votes = random.sample(vote_set, len(vote_set))
    for c1, c2, result in shuffled_votes:
        # For now, ignore ties. This probably could be improved - ties do give us information
        if result == "tie":
            continue

        # Ensure that c1 is the victor and c2 the loser, by swapping if they are a loss
        if result == "loss":
            c1, c2 = c2, c1

        win_graph.add_edge(c1, c2)

    # convert to DAG by removing edges from every cycle
    while True:
        try:
            cycles = nx.find_cycle(win_graph)
            # If we hit this line, a NoCycle exception was not thrown, therefore there is a cycle and we have to
            # remove an edge from it
            win_graph.remove_edge(*cycles[random.randint(0, len(cycles) - 1)])
        except nx.NetworkXNoCycle:
            break

    assert nx.is_directed_acyclic_graph(win_graph)
    return win_graph
