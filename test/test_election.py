from socialchoice import Election

example_votes = [[0, 1, "win"], [3, 2, "loss"], [2, 3, "win"], [0, 3, "tie"], [3, 0, "win"]]
example_candidates = {0, 1, 2, 3}

def test_add_votes():
    e = Election()
    e.add_votes()
    assert e.get_votes() == []
    e.add_votes(example_votes[0])
    assert e.get_votes() == [[0, 1, "win"]]
    e.add_votes(*example_votes[1:])
    assert e.get_votes() == example_votes


def test_get_votes():
    e = Election()
    assert e.get_votes() == []
    e.add_votes(*example_votes)
    assert e.get_votes() == example_votes

    e1 = Election(*(example_votes[1:]))
    assert e1.get_votes() == example_votes[1:]


def test_get_candidates():
    e = Election()
    assert e.get_candidates() == set()
    e.add_votes(*example_votes)
    assert e.get_candidates() == example_candidates
    e1 = Election(*example_votes)
    assert e1.get_candidates() == example_candidates


def test_get_victory_graph():
    e = Election()
    assert len(e.get_victory_graph()) == 0


def test_get_matchup_graph():
    e = Election()
    assert len(e.get_matchup_graph()) == 0


def test_get_matchups():
    e_empty = Election()
    assert e_empty.get_matchups() == {}

    e_1 = Election(*example_votes)
    assert e_1.get_matchups() == {0: {1: {'wins': 1, 'losses': 0, 'ties': 0},
                                      2: {'wins': 0, 'losses': 0, 'ties': 0},
                                      3: {'wins': 0, 'losses': 1, 'ties': 1}},
                                  1: {0: {'wins': 0, 'losses': 1, 'ties': 0},
                                      2: {'wins': 0, 'losses': 0, 'ties': 0},
                                      3: {'wins': 0, 'losses': 0, 'ties': 0}},
                                  2: {0: {'wins': 0, 'losses': 0, 'ties': 0},
                                      1: {'wins': 0, 'losses': 0, 'ties': 0},
                                      3: {'wins': 2, 'losses': 0, 'ties': 0}},
                                  3: {0: {'wins': 1, 'losses': 0, 'ties': 1},
                                      1: {'wins': 0, 'losses': 0, 'ties': 0},
                                      2: {'wins': 0, 'losses': 2, 'ties': 0}}}


def test_get_ranked_pairs_ranking():
    e_empty = Election()
    assert e_empty.get_ranked_pairs_ranking() == []

    e_1 = Election(*example_votes)
    assert e_1.get_ranked_pairs_ranking() == [2, 3, 0, 1]


def test_get_win_ratio():
    e_empty = Election()
    assert e_empty.get_win_ratio() == []

    e_1 = Election(*example_votes)
    assert e_1.get_win_ratio() == [(2, 1.0), (0, 0.5), (3, 1/3), (1, 0.0)]

def test_get_win_tie_ratio():
    e_empty = Election()
    assert e_empty.get_win_tie_ratio() == []

    e_1 = Election(*example_votes)
    assert e_1.get_win_tie_ratio() == [(2, 1.0), (0, 2/3), (3, 0.5), (1, 0.0)]
