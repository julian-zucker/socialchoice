"""This file computes the values in the "Results" section of the vote induction paper."""
import csv
import multiprocessing

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

    # Each voter should have equal weight, so make each vote set the same size
    for voter in voter_to_vote_set:
        voter_to_vote_set[voter] = random.choices(voter_to_vote_set[voter], k=num_pairs)
        # Also update the pairwise dataset to reflect the new votes
    dataset = [vote for vote_set in voter_to_vote_set.values() for vote in vote_set]

    # This is the pairwise election that serves as a baseline "ground truth" for the
    # vote induction method.
    pairwise_election = Election(PairwiseBallotBox([vote[0:3] for vote in dataset]))

    transitive_vote_sets = [
        intransitivity_resolver(vote_set) for vote_set in voter_to_vote_set.values()
    ]

    complete_vote_sets = []

    for vote_graph in transitive_vote_sets:
        complete_vote_sets.append(incompleteness_resolver(vote_graph, candidates))

    # Create an election using the Ranked ballots
    ranked_choice_ballots = [
        list(nx.topological_sort(win_graph)) for win_graph in complete_vote_sets
    ]
    ranking_election = Election(RankedChoiceBallotBox(ranked_choice_ballots))

    pairwise_ranking = pairwise_election.ranking_by_ranked_pairs()
    ranked_choice_ranking = ranking_election.ranking_by_ranked_pairs()

    tau = ranking_similarity.kendalls_tau(pairwise_ranking, ranked_choice_ranking)
    print(f"tau={tau},{intransitivity_resolver.__name__},{incompleteness_resolver.__name__}")


if __name__ == "__main__":
    with open("../data/dog_project_votes.csv") as csv_fd:
        dog_project_votes = [row for row in csv.reader(csv_fd)]

    wg = PairwiseBallotBox([v[0:3] for v in dog_project_votes]).get_matchup_graph()
    edge_to_weight = {e: wg.get_edge_data(*e)["margin"] for e in wg.edges}
    vote_sets = [dog_project_votes]

    intransitivity_resolvers = [
        break_random_link,
        make_break_weakest_link(edge_to_weight),
        make_add_edges_in_order(edge_to_weight),
    ]

    incompleteness_resolvers = [
        place_randomly,
        add_random_edges,
        make_add_edges_by_win_ratio(edge_to_weight),
    ]

    # The set of inputs to run kendall_tau_distance on is the cartesian product of the above arrays
    inputs = []
    for vote_set in vote_sets:
        for int_res in intransitivity_resolvers:
            for inc_res in incompleteness_resolvers:
                # Run 30 times to cut down noise due to stochastic problems
                multiprocessing.Pool().starmap(
                    evaluate_vote_induction_method, [(vote_set, int_res, inc_res)] * 30
                )
