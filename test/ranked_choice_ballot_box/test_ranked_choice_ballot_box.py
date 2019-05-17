import pytest

from socialchoice import RankedChoiceBallotBox, Election


@pytest.fixture
def election():
    example_votes = RankedChoiceBallotBox([
        [{1}, {2}, {3}, {4}],
        [{1}, {3}, {2}, {4}],
        [{1}, {2}, {3}, {4}],
        [{1}, {2}, {4}, {3}]
    ])
    return Election(example_votes)


# Two tests considered sufficient for now because  ranked choice is implemented in terms of PairwiseBallotBox,
# which we have many tests for.

def test_ranked_pairs_on_ranked_choice(election):
    ranking = election.ranking_by_ranked_pairs()

    assert ranking == [1, 2, 3, 4]


def test_copeland_on_ranked_choice(election):
    ranking = election.ranking_by_copeland(include_score=True)

    assert ranking == [(1, 3), (2, 1), (3, -1), (4, -3)]

    ranking_no_score = election.ranking_by_copeland()
    assert ranking_no_score == [1, 2, 3, 4]
