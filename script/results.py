"""This file computes the values in the "Results" section of the vote induction paper."""
import csv
import multiprocessing
import sys

from socialchoice import Election, RankedChoiceBallotBox, ranking_similarity
from socialchoice.induction.resolving_incompleteness import *
from socialchoice.induction.resolving_intransitivity import *


def evaluate_vote_induction_method(dataset, intransitivity_resolver, incompleteness_resolver):
    """Computes the Kendall tau distance between original pairwise votes from a dataset and the collapsed rankings.
    Uses the Kendall tau on the output of the specified social choice method.

    :param dataset: a list of 4-tuples, each representing a pairwise vote followed by a voter uuid
    :param intransitivity_resolver: a function that takes a win-graph and returns an acyclic win-graph
    :param incompleteness_resolver: a function that takes a win-graph and a set of candidates
    and produces a fully-connected win-graph with each candidate
    :return: a float in [-1, 1]
    """
    voter_to_vote_set = {vote[3]: [] for vote in dataset}
    candidates = {v[0] for v in dataset} | {v[1] for v in dataset}
    num_pairs = len(candidates) * (len(candidates) - 1) // 2

    # vote_sets should be a mapping from each voter to the contents of each of their votes.
    for vote in dataset:
        voter_to_vote_set[vote[3]].append(vote[0:3])

    # This is the pairwise election that serves as a baseline "ground truth" for the
    # vote induction method.
    pairwise_election = Election(PairwiseBallotBox([vote[0:3] for vote in dataset]))

    ranked_choice_ballots = []
    for vote_set in voter_to_vote_set.values():
        transitive_votes = intransitivity_resolver(vote_set)
        complete_votes = incompleteness_resolver(transitive_votes)
        ordering = list(nx.topological_sort(complete_votes))
        ranked_choice_ballots.append(ordering)

    ranking_election = Election(RankedChoiceBallotBox(ranked_choice_ballots))

    pairwise_ranking = pairwise_election.ranking_by_ranked_pairs()
    ranked_choice_ranking = ranking_election.ranking_by_ranked_pairs()

    tau = ranking_similarity.kendalls_tau(pairwise_ranking, ranked_choice_ranking)
    print(
        f"tau={tau},{intransitivity_resolver.func.__name__},{incompleteness_resolver.func.__name__}"
    )


if __name__ == "__main__":
    with open(sys.argv[1]) as csv_fd:
        dog_project_votes = [row for row in csv.reader(csv_fd)]

    ballots = PairwiseBallotBox([v[0:3] for v in dog_project_votes])

    intransitivity_factory = IntransitivityResolverFactory(ballots)
    intransitivity_resolvers = [
        intransitivity_factory.make_break_random_link(),
        intransitivity_factory.make_break_weakest_link(),
        intransitivity_factory.make_add_edges_in_order(),
    ]

    incompleteness_factory = IncompletenessResolverFactory(ballots)
    incompleteness_resolvers = [
        incompleteness_factory.make_place_randomly(),
        incompleteness_factory.make_add_edges_by_win_ratio(),
        incompleteness_factory.make_add_random_edges(),
    ]

    # The set of inputs to run kendall_tau_distance on is the cartesian product of the above arrays
    inputs = []
    for int_res in intransitivity_resolvers:
        for inc_res in incompleteness_resolvers:
            # Run 30 times to reduce noise
            with multiprocessing.Pool() as p:
                p.starmap(
                    evaluate_vote_induction_method, [(dog_project_votes, int_res, inc_res)] * 30
                )
