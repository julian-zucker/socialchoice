import pytest

from socialchoice import PairwiseBallotBox, nx
from socialchoice.induction.resolving_incompleteness import IncompletenessResolverFactory


@pytest.fixture
def factory():
    votes = PairwiseBallotBox(
        [(1, 2, "win")] * 10
        + [(1, 3, "win")] * 10
        + [(2, 3, "win")] * 10
        + [(2, 1, "win")] * 15
        + [(3, 1, "win")] * 10
        + [(3, 2, "win")] * 11
    )
    return IncompletenessResolverFactory(votes)


@pytest.fixture
def wg():
    # A simple, empty win graph to fill. Technically transitive, so these methods shouldn't choke.
    return nx.DiGraph()


def test_factory_producing_place_randomly(factory, wg):
    wg = factory.make_place_randomly()(wg)
    assert len(wg.nodes) == 3
    assert len(wg.edges) == 3


def test_factory_producing_add_all_at_beginning(factory, wg):
    wg = factory.make_add_all_at_beginning()(wg)
    assert len(wg.nodes) == 3
    assert len(wg.edges) == 0


def test_factory_producing_add_all_at_end(factory, wg):
    wg = factory.make_add_all_at_end()(wg)

    assert len(wg.nodes) == 3
    assert len(wg.edges) == 0


def test_factory_producing_add_random_edges(factory, wg):
    wg = factory.make_add_random_edges()(wg)

    assert len(wg.nodes) == 3
    assert len(wg.edges) == 3


def test_factory_producing_add_edges_by_win_ratio(factory, wg):
    wg = factory.make_add_edges_by_win_ratio()(wg)
    assert len(wg.nodes) == 3
    assert len(wg.edges) == 3
    assert set(wg.edges) == {(3, 2), (2, 1), (3, 1)}
