import pytest


from socialchoice.induction.resolving_intransitivity import *


@pytest.fixture
def simple_votes():
    return [(1, 2, "win"), (2, 3, "win"), (3, 1, "win")]


def test_break_random_link(simple_votes):
    result = list(nx.topological_sort(break_random_link(simple_votes)))
    assert result in [[1, 2, 3], [2, 3, 1], [3, 1, 2]]


def test_break_weakest_link(simple_votes):
    edge_weights = {(1, 2): 0.9, (2, 3): 0.8, (3, 1): 0.7}

    break_weakest_link = make_break_weakest_link(edge_weights)

    result = list(nx.topological_sort(break_weakest_link(simple_votes)))
    # (3,1) must be broken, as it is weakest
    assert result == [1, 2, 3]


def test_add_edges_in_order(simple_votes):
    edge_weights = {(1, 2): 0.9, (2, 3): 0.8, (3, 1): 0.7}

    add_edges_in_order = make_add_edges_in_order(edge_weights)
    result = list(nx.topological_sort(add_edges_in_order(simple_votes)))
    # (3,1) must not be chosen, as it is weakest
    assert result == [1, 2, 3]
