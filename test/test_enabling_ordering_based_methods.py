from socialchoice import Election, PairwiseBallotBox
from socialchoice.pairwisecollapse.resolving_incompleteness import add_random_edges
from socialchoice.pairwisecollapse.resolving_intransitivity import break_random_link


def test_simple_pairwise_ballot():
    # Repeat this 100 times to drown out the noise inherent to stochastic pairwise collapse methods
    ballots = PairwiseBallotBox(
        [(1, 2, "win"), (1, 3, "win"), (1, 4, "win"), (3, 4, "win"), (3, 2, "win"), (2, 4, "win")]
        * 100
    )

    ballots.enable_ordering_based_methods(break_random_link, add_random_edges)

    assert Election(ballots).ranking_by_borda_count() == [1, 3, 2, 4]
