import pytest

from socialchoice import *


def test_no_candidate_repeats():
    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 1]])


def test_require_full_ballots_with_candidate_inference():
    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 2, 3, 4], [4, 3, 2, 1], [3, 2, 1]])


def test_requires_full_ballots():
    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 2]], candidates=[1, 2, 3])

    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 2, 3, 4]], candidates=[1, 2, 3])


def test_requires_no_duplicates():
    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, {1}]])

    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[{1}, 1]])

    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 2, {3, 1}]])


def test_candidates_no_duplicates():
    with pytest.raises(InvalidElectionDataException):
        RankedChoiceBallotBox([[1, 2, 3]], candidates=[1, 1, 2, 3])


def test_rankings_can_include_ties():
    RankedChoiceBallotBox([[{1, 2}]])

    RankedChoiceBallotBox([[1, {2, 4}, {3, 5}]])
