import pytest

from pairwise_collapse.resolving_incompleteness import place_randomly
from pairwise_collapse.resolving_intransitivity import break_random_link
from socialchoice import *


def assert_same_rankings(ballot_box_1: BallotBox, ballot_box_2: BallotBox):
    """This function is a test utility that ensures two ballot boxes are roughly equivalent by asserting that they
    have the same rankings by multiple methods.

    :raises: AssertionError if the rankings differ
    """
    e1 = Election(ballot_box_1)
    e2 = Election(ballot_box_2)
    assert e1.ranking_by_ranked_pairs() == e2.ranking_by_ranked_pairs()
    assert e1.ranking_by_win_ratio() == e2.ranking_by_win_ratio()
    assert e1.ranking_by_win_tie_ratio() == e2.ranking_by_win_tie_ratio()
    assert e1.ranking_by_minimax() == e2.ranking_by_minimax()

def test_intransitive_removed():
    pytest.skip("change API, then fix these")
    """If you have three intransitive votes (a minimal cycle), the result should have two of the three."""
    result = pairwise_collapse([(1, 2, "win"), (2, 3, "win"), (3, 1, "win")], {1,2,3}, break_random_link, place_randomly)

    # should still keep most of the structure, so we aren't okay with any of the six options
    assert result in [[1, 2, 3], [2, 3, 1], [3, 1, 2]]

def test_incomplete_transitive_votes_filled_in():
    pytest.skip("change API, then fix theserr")
    """This test shows how a missing 1->3 win isn't an issue if you have 1->2 and 2->3"""
    result = pairwise_collapse([(1, 2, "win"), (2, 3, "win")], {1,2,3}, break_random_link, place_randomly)
    assert result == [1, 2, 3]
