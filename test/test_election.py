from socialchoice import Election, PairwiseBallots

empty_election = Election(PairwiseBallots([]))
example_votes = PairwiseBallots([[0, 1, "win"], [3, 2, "loss"], [2, 3, "win"], [0, 3, "tie"], [3, 0, "win"]])


def test_get_ranked_pairs_ranking():
    assert empty_election.ranking_by_ranked_pairs() == []

    e_1 = Election(example_votes)
    assert e_1.ranking_by_ranked_pairs() == [2, 3, 0, 1]


def test_get_win_ratio():
    assert empty_election.ranking_by_win_ratio() == []

    e_1 = Election(example_votes)
    assert e_1.ranking_by_win_ratio() == [(2, 1.0), (0, 0.5), (3, 1 / 3), (1, 0.0)]


def test_get_win_tie_ratio():
    assert empty_election.ranking_by_win_tie_ratio() == []

    e_1 = Election(example_votes)
    assert e_1.ranking_by_win_tie_ratio() == [(2, 1.0), (0, 2 / 3), (3, 0.5), (1, 0.0)]
