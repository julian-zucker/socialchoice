import random

import pytest
from hypothesis import given, note, strategies as st

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
    """If you have three intransitive votes (a minimal cycle), the result should have two of the three."""
    result = pairwise_collapse([(1, 2, "win"), (2, 3, "win"), (3, 1, "win")])

    # should still keep most of the structure, so we aren't okay with any of the six options
    assert result in [[1, 2, 3], [2, 3, 1], [3, 1, 2]]


def test_incomplete_transitive_votes_filled_in():
    """This test shows how a missing 1->3 win isn't an issue if you have 1->2 and 2->3"""
    result = pairwise_collapse([(1, 2, "win"), (2, 3, "win")])
    assert result == [1, 2, 3]


def test_incomplete_unvoted_elements_in_middle():
    """If there are three candidates, and one vote, the third candidate should go in the middle."""

    result = pairwise_collapse([(1, 2, "win")], candidates={1, 2, 3})
    # Why do unvoted elements go in the middle? We have one bit of evidence against 2, and one bit of evidence towards
    # 1, so 3 ought to be in between.
    assert result == [1, 3, 2]

    # Also testing this with four, but this test I'm willing to give up
    result4 = pairwise_collapse([(1, 4, "win")], candidates={1, 2, 3, 4})
    assert result4 == [1, 2, 3, 4] or result4 == [1, 3, 2, 4]


@pytest.mark.slow
@pytest.mark.hypothesis
@given(
    st.lists(
        st.lists(
            st.sampled_from([(a, b, "win") for a in range(10) for b in range(10) if a != b]),
            min_size=1)
            .map(set)
            .map(list),
        min_size=1, max_size=5000))
def test_pairwise_collapse_equal_to_pairwise_comparisons(pairwise_votes):
    """Tests that on an arbitrary input set with only win votes"""
    note(f"Pairwise votes: {pairwise_votes}")

    pairwise = PairwiseBallotBox(flatten(pairwise_votes))
    if len(pairwise.candidates) == 10:
        ranked = RankedChoiceBallotBox([pairwise_collapse(vote_set, set(range(10))) for vote_set in pairwise_votes])
        assert_same_rankings(pairwise, ranked)


@pytest.mark.slow
def test_pairwise_collapse_equivalent_to_rankings_on_dog_votes():
    pytest.skip("Need performance improvement before running this is valid")
    import csv

    with open("test/data/dog_project_votes.csv") as votes_fd:
        votes = [x for x in csv.reader(votes_fd)]

    pbb = PairwiseBallotBox([vote[0:3] for vote in votes])

    vote_sets = {v[3]: [] for v in votes}

    for vote in votes:
        vote_sets[vote[3]].append(vote[0:3])

    ranks = pairwise_collapse_by_voter(vote_sets.values(), upsample=True)
    rbb = RankedChoiceBallotBox(ranks)

    assert Election(pbb).ranking_by_ranked_pairs() == Election(rbb).ranking_by_ranked_pairs()
