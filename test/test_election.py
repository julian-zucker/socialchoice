from socialchoice import Election

example_votes = [[0, 1, "win"], [3, 2, "loss"], [2, 3, "win"], [0, 3, "tie"], [3, 0, "win"]]
example_candidates = {0, 1, 2, 3}
empty_election = Election([])


def test_get_victory_graph_empty():
    assert len(empty_election.get_victory_graph()) == 0

    complex_victory_graph = Election(example_votes).get_victory_graph()
    assert (0, 1) in complex_victory_graph.edges
    assert (2, 3) in complex_victory_graph.edges
    assert (3, 0) in complex_victory_graph.edges
    assert (1, 0) not in complex_victory_graph.edges

    assert complex_victory_graph.get_edge_data(0, 1) == {"wins": 1, "ties": 0, "losses": 0, "margin": 1}
    assert complex_victory_graph.get_edge_data(3, 0) == {"wins": 1, "ties": 1, "losses": 0, "margin": .5}


def test_get_matchup_graph():
    assert len(empty_election.get_matchup_graph()) == 0

    complex_matchup_graph = Election(example_votes).get_matchup_graph()
    assert (0, 1) in complex_matchup_graph.edges
    assert (1, 0) in complex_matchup_graph.edges
    assert (2, 3) in complex_matchup_graph.edges
    assert (3, 2) in complex_matchup_graph.edges
    assert (3, 0) in complex_matchup_graph.edges
    assert (0, 3) in complex_matchup_graph.edges

    assert complex_matchup_graph.get_edge_data(0, 1) == {"wins": 1, "ties": 0, "losses": 0, "margin": 1}
    assert complex_matchup_graph.get_edge_data(3, 0) == {"wins": 1, "ties": 1, "losses": 0, "margin": .5}


def test_get_matchups():
    e_empty = Election([])
    assert e_empty.get_matchups() == {}

    e_1 = Election(example_votes)
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
