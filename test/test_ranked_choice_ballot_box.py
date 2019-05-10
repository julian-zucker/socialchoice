from socialchoice import RankedChoiceBallotBox, Election

empty_votes = RankedChoiceBallotBox([])

example_votes = RankedChoiceBallotBox([
    [1, 2, 3, 4],
    [1, 3, 2, 4],
    [1, 2, 3, 4],
    [1, 2, 4, 3]
])

example_election = Election(example_votes)

# Two tests considered sufficient for now because of how ranked choice is implemented in terms of PairwiseBallotBox
def test_ranked_pairs_on_ranked_choice():
    ranking = example_election.ranking_by_ranked_pairs()

    assert ranking == [1, 2, 3, 4]


def test_copeland_on_ranked_choice():
    ranking = example_election.ranking_by_copeland()

    assert ranking == [(1, 3), (2, 1), (3, -1), (4, -3)]