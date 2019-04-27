import networkx

from src.socialchoice import Election

example_votes = [[0, 1, "win"], [3, 2, "loss"], [2, 3, "win"], [0, 3, "tie"], [3, 0, "win"]]
example_candidates = {0, 1, 2, 3}

def test_add_votes():
    e = Election()
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


def test_get_victory_graph(self):
    e = Election()
    assert e.get_victory_graph() == networkx.DiGraph()


def test_get_matchup_graph(self):
    e = Election()
    assert e.get_victory_graph() == networkx.DiGraph()


# def test_get_matchups(self):
#     self.fail()
#
#
# def test_get_ranked_pairs_ranking(self):
#     self.fail()
#
#
# def test_ranked_pairs(self):
#     self.fail()
#
#
# def test_copeland(self):
#     self.fail()
#
#
# def test_minimax(self):
#     self.fail()
#
#
# def test_win_ratio(self):
#     self.fail()
#
#
# def test_win_tie_ratio(self):
#     self.fail()
