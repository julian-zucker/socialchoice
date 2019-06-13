import pytest

from socialchoice import (
    PairwiseBallotBox,
    InvalidBallotDataException,
    VoterTrackingPairwiseBallotBox,
)

empty_votes = VoterTrackingPairwiseBallotBox([])
example_votes = VoterTrackingPairwiseBallotBox(
    [
        [0, 1, "win", "voter1"],
        [3, 2, "loss", "voter1"],
        [2, 3, "win", "voter1"],
        [0, 3, "tie", "voter1"],
        [3, 0, "win", "voter1"],
    ]
)


def test_get_matchups():
    assert empty_votes.get_matchups() == {}

    assert example_votes.get_matchups() == {
        0: {
            1: {"wins": 1, "losses": 0, "ties": 0},
            2: {"wins": 0, "losses": 0, "ties": 0},
            3: {"wins": 0, "losses": 1, "ties": 1},
        },
        1: {
            0: {"wins": 0, "losses": 1, "ties": 0},
            2: {"wins": 0, "losses": 0, "ties": 0},
            3: {"wins": 0, "losses": 0, "ties": 0},
        },
        2: {
            0: {"wins": 0, "losses": 0, "ties": 0},
            1: {"wins": 0, "losses": 0, "ties": 0},
            3: {"wins": 2, "losses": 0, "ties": 0},
        },
        3: {
            0: {"wins": 1, "losses": 0, "ties": 1},
            1: {"wins": 0, "losses": 0, "ties": 0},
            2: {"wins": 0, "losses": 2, "ties": 0},
        },
    }


def test_get_victory_graph_empty():
    assert len(empty_votes.get_victory_graph()) == 0

    complex_victory_graph = example_votes.get_victory_graph()
    assert (0, 1) in complex_victory_graph.edges
    assert (2, 3) in complex_victory_graph.edges
    assert (3, 0) in complex_victory_graph.edges
    assert (1, 0) not in complex_victory_graph.edges

    assert complex_victory_graph.get_edge_data(0, 1) == {
        "wins": 1,
        "ties": 0,
        "losses": 0,
        "margin": 1,
    }
    assert complex_victory_graph.get_edge_data(3, 0) == {
        "wins": 1,
        "ties": 1,
        "losses": 0,
        "margin": 0.5,
    }


def test_get_matchup_graph():
    assert len(empty_votes.get_matchup_graph()) == 0

    complex_matchup_graph = example_votes.get_matchup_graph()
    assert (0, 1) in complex_matchup_graph.edges
    assert (1, 0) in complex_matchup_graph.edges
    assert (2, 3) in complex_matchup_graph.edges
    assert (3, 2) in complex_matchup_graph.edges
    assert (3, 0) in complex_matchup_graph.edges
    assert (0, 3) in complex_matchup_graph.edges

    assert complex_matchup_graph.get_edge_data(0, 1) == {
        "wins": 1,
        "ties": 0,
        "losses": 0,
        "margin": 1,
    }
    assert complex_matchup_graph.get_edge_data(3, 0) == {
        "wins": 1,
        "ties": 1,
        "losses": 0,
        "margin": 0.5,
    }


def test_throws_error_on_wrong_ballot_length():
    with pytest.raises(InvalidBallotDataException):
        PairwiseBallotBox([("a", "b", "win", "fourth thing")])

    with pytest.raises(InvalidBallotDataException):
        PairwiseBallotBox([[]])

    with pytest.raises(InvalidBallotDataException):
        # Third element must be win/tie/loss
        PairwiseBallotBox([("a", "b", "foo")])

    PairwiseBallotBox([("a", "b", "win"), ("a", "b", "loss"), ("a", "b", "tie")])
