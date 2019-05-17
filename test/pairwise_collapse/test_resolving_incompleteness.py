import pytest

from pairwise_collapse.resolving_incompleteness import *


@pytest.fixture
def win_graph():
    wg = nx.DiGraph()
    wg.add_nodes_from([1, 2])
    wg.add_edge(1, 2)
    return wg


@pytest.fixture
def candidates_to_add():
    return {3}


def test_place_randomly(win_graph, candidates_to_add):
    results = list()
    for i in range(100):
        results.append(place_randomly(win_graph, candidates_to_add))

    # using tuples so they are hashable
    rankings = {tuple(nx.topological_sort(wg)) for wg in results}

    assert (3, 1, 2) in rankings
    assert (1, 3, 2) in rankings
    assert (1, 2, 3) in rankings
    assert len(rankings) == 3


def test_add_all_at_beginning(win_graph, candidates_to_add):
    result = list(nx.topological_sort(add_all_at_beginning(win_graph, candidates_to_add)))
    assert result == [3, 1, 2]


def test_add_all_at_end(win_graph, candidates_to_add):
    result = list(nx.topological_sort(add_all_at_end(win_graph, candidates_to_add)))
    assert result == [1, 2, 3]


def test_add_random_edges(win_graph, candidates_to_add):
    results = list()
    for i in range(100):
        results.append(place_randomly(win_graph, candidates_to_add))

    rankings = {tuple(nx.topological_sort(wg)) for wg in results}

    assert (3, 1, 2) in rankings
    assert (1, 3, 2) in rankings
    assert (1, 2, 3) in rankings
    assert len(rankings) == 3


def test_add_edges_by_win_ratio(win_graph, candidates_to_add):
    edges_by_win_ratio = [(2, 1), (1, 3), (3, 2), (2, 3), (1, 2), (1, 2)]
    add_edges_by_win_ratio = make_add_edges_by_win_ratio(edges_by_win_ratio)
    result = list(nx.topological_sort(add_edges_by_win_ratio(win_graph, candidates_to_add)))

    # Edges (1,3) and (3,2) will be added, so this result is required
    assert result == [1, 3, 2]
