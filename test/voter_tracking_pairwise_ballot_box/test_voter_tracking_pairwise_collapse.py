from socialchoice import (
    VoterTrackingPairwiseBallotBox,
    IntransitivityResolverFactory,
    IncompletenessResolverFactory,
    Election,
)


def test_pairwise_collapse_different_voters():
    # If each vote is from a different person, most outcomes are possible

    votes = [
        [0, 1, "win", "voter1"],
        [1, 2, "win", "voter2"],
        [2, 0, "loss", "voter3"],
        [2, 3, "win", "voter4"],
        [1, 3, "tie", "voter5"],
        [0, 3, "win", "voter6"],
    ]
    ballots = VoterTrackingPairwiseBallotBox(votes)

    intransitivity_res = IntransitivityResolverFactory(ballots).make_break_random_link()
    incompleteness_res = IncompletenessResolverFactory(ballots).make_add_random_edges()

    orderings = set()

    for _ in range(100):
        # Make a new one to avoid mutation
        ballots = VoterTrackingPairwiseBallotBox(votes)
        ballots.enable_ordering_based_methods(intransitivity_res, incompleteness_res)
        orderings.add(tuple(Election(ballots).ranking_by_borda_count()))

    assert len(orderings) > 12

    votes_v1 = [vote[0:3] + ["voter1"] for vote in votes]
    ballots_v1 = VoterTrackingPairwiseBallotBox(votes_v1)

    intransitivity_res = IntransitivityResolverFactory(ballots_v1).make_break_random_link()
    incompleteness_res = IncompletenessResolverFactory(ballots_v1).make_add_random_edges()

    orderings = set()

    for _ in range(100):
        ballots_v1 = VoterTrackingPairwiseBallotBox(votes_v1)
        ballots_v1.enable_ordering_based_methods(intransitivity_res, incompleteness_res)
        orderings.add(tuple(Election(ballots_v1).ranking_by_borda_count()))

    assert len(orderings) < 12
