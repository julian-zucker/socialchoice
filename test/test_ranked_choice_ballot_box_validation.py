import pytest

from socialchoice import *


def test_only_allows_specified_candidates_on_ballots():
    RankedChoiceBallotBox([[1, 2], [2, 3]], candidates=[1, 2, 3])

    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 2]], candidates=[1])


def test_no_candidate_repeats():
    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 1]])


def test_require_full_ballots_with_candidate_inference():
    RankedChoiceBallotBox([[1,2,3,4], [4,3,2,1], [3,2,1]])

    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1,2,3,4], [4,3,2,1], [3,2,1]], require_full_ballots=True)

def test_ensures_full_ballots_if_asked():
    RankedChoiceBallotBox([[1, 2]], candidates=[1, 2, 3])

    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 2]], candidates=[1, 2, 3], require_full_ballots=True)

    with pytest.raises(InvalidBallotDataException):
        RankedChoiceBallotBox([[1, 2, 3, 4]], candidates=[1, 2, 3], require_full_ballots=True)

def test_candidates_no_duplicates():
    with pytest.raises(InvalidElectionDataException):
        RankedChoiceBallotBox([[1, 2, 3]], candidates=[1, 1, 2, 3])
