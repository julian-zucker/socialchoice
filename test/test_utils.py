import networkx as nx
from hypothesis import given
from hypothesis import strategies as st

from socialchoice import PairwiseBallotBox
from socialchoice.util import ranking_with_all_sets, ranking_to_pairwise_ballots


def test_ranking_with_all_sets():
    assert ranking_with_all_sets([1, 2, 3]) == [{1}, {2}, {3}]
    assert ranking_with_all_sets([1, {2, 3}]) == [{1}, {2, 3}]
    assert ranking_with_all_sets([{1}, {2, 3}]) == [{1}, {2, 3}]


def test_ranking_to_pairwise_ballots():
    assert set(ranking_to_pairwise_ballots([1, 2])) == {(1, 2, "win")}
    assert set(ranking_to_pairwise_ballots([1, 2, 3])) == {
        (1, 2, "win"),
        (1, 3, "win"),
        (2, 3, "win"),
    }
    assert set(ranking_to_pairwise_ballots([1, {2, 3}])) == {
        (1, 2, "win"),
        (1, 3, "win"),
        (2, 3, "tie"),
    }
    assert set(ranking_to_pairwise_ballots([{1, 2}, {3, 4}])) == {
        (1, 2, "tie"),
        (1, 3, "win"),
        (1, 4, "win"),
        (2, 3, "win"),
        (2, 4, "win"),
        (3, 4, "tie"),
    }


@given(st.lists(st.integers(), unique=True, min_size=2))
def test_pairwise_ballots_roundtrip(ranking):
    """Converting a ranking to pairwise ballots and then toposorting will produce the same ranking"""

    pairwise = ranking_to_pairwise_ballots(ranking)
    pairwise_ranked_pairs = list(
        nx.topological_sort(PairwiseBallotBox(pairwise).get_victory_graph())
    )
    assert pairwise_ranked_pairs == ranking
