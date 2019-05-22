"""This file computes the values in the "Results" section of the pairwise collapse paper."""
import csv
import random

from socialchoice import ranking_similarity
from socialchoice import RankedChoiceBallotBox
from socialchoice import Election
from pairwise_collapse.resolving_intransitivity import *
from pairwise_collapse.resolving_incompleteness import *

import multiprocessing


def kendall_tau_distance(
    dataset,
    intransitivity_resolver,
    incompleteness_resolver,
    upsampling_method,
    social_choice_method,
):
    """Computes the Kendall tau distance between original pairwise votes from a dataset and the collapsed rankings.
    Uses the Kendall tau on the output of the specified social choice method.

    :param dataset: a list of 4-tuples, each representing a pairwise vote followed by a voter uuid
    :param intransitivity_resolver: a function that takes a win-graph and returns an acyclic win-graph
    :param incompleteness_resolver: a function that takes a win-graph and a set of candidates
    and produces a fully-connected win-graph with each candidate
    :param upsampling_method: the method to upsample with, either "by_voter", "by_vote", or "none"
    :param social_choice_method: the name of the social choice method to run
    :return: a float in [-1, 1]
    """
    vote_sets = {vote[3]: [] for vote in dataset}
    candidates = {v[0] for v in dataset} | {v[1] for v in dataset}
    num_pairs = len(candidates) * (len(candidates) - 1) // 2

    for vote in dataset:
        vote_sets[vote[3]].append(vote[0:3])

    # Each voter should have equal weight, so make each vote set the same size
    if upsampling_method == "by_voter":
        for voter in vote_sets:
            vote_sets[voter] = random.choices(vote_sets[voter], k=num_pairs)
            # Also update the pairwise dataset to reflect the new votes
        dataset = [vote for vote_set in vote_sets.values() for vote in vote_set]

    pairwise_election = Election(PairwiseBallotBox([vote[0:3] for vote in dataset]))

    transitive_vote_sets = [intransitivity_resolver(vote_set) for vote_set in vote_sets.values()]

    complete_vote_sets = []

    for vote_graph in transitive_vote_sets:
        if upsampling_method == "by_vote":
            # We need to put in one ranking per vote in the voter's vote set, but we repeat the ranking to avoid
            # expensive recomputation of the incompleteness resolver
            complete_vote_sets += [incompleteness_resolver(vote_graph, candidates)] * len(
                vote_graph
            )
        else:
            complete_vote_sets.append(incompleteness_resolver(vote_graph, candidates))

    ranked_choice_ballots = [
        list(nx.topological_sort(win_graph)) for win_graph in complete_vote_sets
    ]
    ranking_election = Election(RankedChoiceBallotBox(ranked_choice_ballots))

    if social_choice_method == "ranked_pairs":
        pairwise_ranking = pairwise_election.ranking_by_ranked_pairs()
        ranked_choice_ranking = ranking_election.ranking_by_ranked_pairs()
    elif social_choice_method == "win_ratio":
        pairwise_ranking = pairwise_election.ranking_by_win_ratio()
        ranked_choice_ranking = ranking_election.ranking_by_win_ratio()
    elif social_choice_method == "minimax":
        pairwise_ranking = pairwise_election.ranking_by_minimax()
        ranked_choice_ranking = ranking_election.ranking_by_minimax()
    else:
        raise ValueError(f"Invalid social_choice_method: {social_choice_method}")

    print(pairwise_ranking)
    print(ranked_choice_ranking)
    tau = ranking_similarity.kendalls_tau(pairwise_ranking, ranked_choice_ranking)
    print(
        f"{intransitivity_resolver} {incompleteness_resolver} {upsampling_method} {social_choice_method}: tau={tau}"
    )


# The goal is that this file can be structured like:
# kendall_tau_distance(dogs, break_random_link, place_randomly, upsampling="by_voter", "ranked_pairs")
# repeated for each value required in the table.


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
        add_all_at_beginning,
        add_all_at_end,
        add_random_edges,
        make_add_edges_by_win_ratio(edge_to_weight),
    ]

    upsampling_methods = [
        "by_voter",
        "by_vote",
        # "none",
    ]

    social_choice_methods = [
        "ranked_pairs",
        # "win_ratio",
    ]

    # The set of inputs to run kendall_tau_distance on is the cartesian product of the above arrays
    inputs = []
    for vote_set in vote_sets:
        for int_res in intransitivity_resolvers:
            for inc_res in incompleteness_resolvers:
                for upsample in upsampling_methods:
                    for scm in social_choice_methods:
                        inputs.append((vote_set, int_res, inc_res, upsample, scm))

    pool = multiprocessing.Pool(8)
    out = pool.starmap(kendall_tau_distance, inputs)
