"""This file computes the values in the "Results" section of the pairwise collapse paper."""
import csv
import random

import ranking_similarity
import util
from ballot import PairwiseBallotBox, RankedChoiceBallotBox
from election import Election
from pairwise_collapse.pairwise_collapse import pairwise_collapse_by_voter
from pairwise_collapse.resolving_intransitivity import *
from pairwise_collapse.resolving_incompleteness import *


def kendall_tau_distance(dataset,
                         intransitivity_resolver,
                         incompleteness_resolver,
                         upsampling_method,
                         social_choice_method):
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
            complete_vote_sets += [incompleteness_resolver(vote_graph, candidates)] * len(vote_graph)
        else:
            complete_vote_sets.append(incompleteness_resolver(vote_graph, candidates))

    ranked_choice_ballots = [list(nx.topological_sort(win_graph)) for win_graph in complete_vote_sets]
    ranking_election = Election(RankedChoiceBallotBox(ranked_choice_ballots))

    if social_choice_method == "ranked_pairs":
        ranking1 = pairwise_election.ranking_by_ranked_pairs()
        ranking2 = ranking_election.ranking_by_ranked_pairs()
    elif social_choice_method == "win_ratio":
        ranking1 = pairwise_election.ranking_by_win_ratio()
        ranking2 = ranking_election.ranking_by_win_ratio()
    elif social_choice_method == "minimax":
        ranking1 = pairwise_election.ranking_by_minimax()
        ranking2 = ranking_election.ranking_by_minimax()
    else:
        raise ValueError(f"Invalid social_choice_method: {social_choice_method}")

    print(ranking1)
    print(ranking2)
    tau = ranking_similarity.kendalls_tau(ranking1, ranking2)
    print(f"{intransitivity_resolver} {incompleteness_resolver} {upsampling_method} {social_choice_method}: tau={tau}")


# The goal is that this file can be structured like:
# kendall_tau_distance(dogs, break_random_link, place_randomly, upsampling="by_voter", "ranked_pairs")
# repeated for each value required in the table.

if __name__ == "__main__":
    with open("../data/dog_project_votes.csv") as csv_fd:
        votes = [row for row in csv.reader(csv_fd)]

    wg = PairwiseBallotBox([v[0:3] for v in votes]).get_matchup_graph()
    edge_to_weight = {e: wg.get_edge_data(*e)["margin"] for e in wg.edges}

    datasets = [
        votes
    ]

    intransitivity_resolvers = [
        break_random_link,
        # make_break_weakest_link(edge_to_weight),
        make_add_edges_in_order(edge_to_weight),
    ]

    incompleteness_resolvers = [
        place_randomly,
        # add_all_at_beginning,
        # add_all_at_end,
        # add_random_edges,
        make_add_edges_by_win_ratio(edge_to_weight),
    ]

    upsampling_methods = [
        # "by_voter",
        # "by_vote",
        "none",
    ]

    social_choice_methods = [
        "ranked_pairs",
        "win_ratio",
    ]

    for dataset in datasets:
        for int_res in intransitivity_resolvers:
            for inc_res in incompleteness_resolvers:
                for upsample in upsampling_methods:
                    for scm in social_choice_methods:
                        kendall_tau_distance(dataset, int_res, inc_res, upsample, scm)

# ['57', '20', '65', '40', '37', '35', '70', '43', '45', '28', '34', '52', '54', '27', '24', '25', '51', '44', '48', '74', '56', '38', '72', '26', '68', '69']
# ['57', '20', '65', '40', '37', '35', '70', '43', '45', '28', '34', '52', '54', '27', '24', '25', '51', '44', '48', '74', '56', '38', '72', '26', '68', '69']
# <add_edges_in_order add_edges_by_win_ratio by_voter ranked_pairs:
# tau=KendalltauResult(correlation=1.0, pvalue=4.9591925264495945e-27)
# ['57', '20', '65', '40', '70', '37', '35', '43', '45', '34', '52', '28', '25', '54', '27', '24', '51', '44', '48', '38', '56', '74', '72', '26', '68', '69']
# ['20', '57', '65', '40', '37', '70', '35', '43', '45', '34', '52', '28', '25', '54', '27', '24', '51', '44', '48', '74', '56', '38', '72', '26', '68', '69']
# add_edges_in_order add_edges_by_win_ratio by_voter win_ratio:
# tau=KendalltauResult(correlation=0.9692307692307693, pvalue=6.885987598751056e-22)
