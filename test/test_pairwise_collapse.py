from hypothesis import given, note
from hypothesis import strategies as st
from more_itertools import flatten

from socialchoice import *
from pairwise_collapse import pairwise_collapse


def assert_same_rankings(ballot_box_1: BallotBox, ballot_box_2: BallotBox):
    e1 = Election(ballot_box_1)
    e2 = Election(ballot_box_2)
    assert e1.ranking_by_ranked_pairs() == e2.ranking_by_ranked_pairs()
    assert e1.ranking_by_win_ratio() == e2.ranking_by_win_ratio()
    assert e1.ranking_by_win_tie_ratio() == e2.ranking_by_win_tie_ratio()
    assert e1.ranking_by_minimax() == e2.ranking_by_minimax()


# Tests that in a cycle, the output isn't intransitive
def test_intransitive_removed():
    result = pairwise_collapse([(1, 2, "win"), (2, 3, "win"), (3, 1, "win")])

    # should still keep most of the structure, so we aren't okay with any of the six options
    assert result in [[1, 2, 3], [2, 3, 1], [3, 1, 2]]


def test_incomplete_transitive_votes_filled_in():
    """This test shows how a missing 1->3 win isn't an issue if you have 1->2 and 2->3"""
    result = pairwise_collapse([(1, 2, "win"), (2, 3, "win")])
    assert result == [1, 2, 3]


def test_incomplete_unvoted_elements_in_middle():
    result = pairwise_collapse([(1, 2, "win")], candidates={1, 2, 3})
    # Why do unvoted elements go in the middle? We have one bit of evidence against 2, and one bit of evidence towards
    # 1, so 3 ought to be in between.
    assert result == [1, 3, 2]

    result4 = pairwise_collapse([(1, 4, "win")], candidates={1, 2, 3, 4})
    assert result4 == [1, 2, 3, 4] or result4 == [1, 3, 2, 4]


@given(
    st.lists(
        st.lists(
            st.sampled_from([(a, b, "win") for a in range(10) for b in range(10) if a != b]),
            min_size=1),
        min_size=1, max_size=500))
def test_pairwise_collapse_equal_to_pairwise_comparisons(pairwise_votes):
    pairwise_votes = [list(set(x)) for x in pairwise_votes]
    note(f"Pairwise votes: {pairwise_votes}")

    pairwise = PairwiseBallotBox(flatten(pairwise_votes))

    if len(pairwise.get_matchups()) == 10:
        ranked = RankedChoiceBallotBox([pairwise_collapse(vote_set, set(range(10))) for vote_set in pairwise_votes])
        assert_same_rankings(pairwise, ranked)
