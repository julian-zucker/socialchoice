from socialchoice import PairwiseBallotBox
from socialchoice.induction.resolving_intransitivity import IntransitivityResolverFactory


def test_factory_producing_break_random_link():
    votes = PairwiseBallotBox([(1, 2, "win"), (2, 3, "win"), (3, 1, "win")])

    factory = IntransitivityResolverFactory(votes)
    break_random_link = factory.make_break_random_link()

    transitive = break_random_link(votes.ballots)
    assert len(transitive.edges) == 2


def test_factory_producing_break_weakest_link():
    # (3,1) is the weakest link here, not 100% win ratio
    votes = PairwiseBallotBox(
        [(1, 2, "win"), (1, 2, "win"), (2, 3, "win"), (2, 3, "win"), (3, 1, "win"), (3, 1, "tie")]
    )

    factory = IntransitivityResolverFactory(votes)
    break_weakest_link = factory.make_break_weakest_link()

    transitive = break_weakest_link(votes.ballots)
    assert set(transitive.edges) == {(1, 2), (2, 3)}


def test_factory_producing_add_edges_in_order():
    # (3,1) is the weakest link here, not 100% win ratio
    votes = PairwiseBallotBox(
        [(1, 2, "win"), (1, 2, "win"), (2, 3, "win"), (2, 3, "win"), (3, 1, "win"), (3, 1, "tie")]
    )

    factory = IntransitivityResolverFactory(votes)
    add_edges_in_order = factory.make_add_edges_in_order()

    transitive = add_edges_in_order(votes.ballots)
    assert set(transitive.edges) == {(1, 2), (2, 3)}
