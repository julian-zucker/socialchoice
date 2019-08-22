import functools

import networkx as nx
import util
from ballot import BallotBox


def optional_score(ranking_method):
    """Adds a flag to include or remove the score from a ranking method that returns a list of 2-tuples,
    where the first element is the candidate, and the second element is a score.

    :param ranking_method: a method on an Election
    :return: the same ranking method, but with a flag `include_score`, which defaults to False. If set to true, the
    function returns a list of 2-tuples instead of just a ranking
    """

    # This unfortunately has to be defined above Election to be used in Election

    def nest_ties(ranking):
        """
        >>> nest_ties([("a", 1), ("b", 1), ("c", 0)])
        [[("a", 1), ("b", 1)], [("c", 0)]]

        :param ranking: A list of 2-tuples of (item, score)
        :return: a list of lists of 2-tuples, where each list in the outer list contains only items with the same score.
        """
        if len(ranking) == 0:
            return ranking

        out = []
        current_tie = [ranking[0]]
        for item, score in ranking[1:]:
            # There are no items in the current tied set, or the score of the current item is the same
            if current_tie[0][0] == score:
                current_tie.append((item, score))
            else:
                out.append(current_tie)
                current_tie = [(item, score)]
        return out

    @functools.wraps(ranking_method)
    def wrapped_ranking_method(self, include_score=False, group_ties=False):
        ranking = ranking_method(self)

        if include_score and group_ties:
            return nest_ties(ranking)
        elif include_score and not group_ties:
            return ranking
        elif not include_score and group_ties:
            return [item for tie_group in nest_ties(ranking) for item, score in tie_group]
        elif not include_score and not group_ties:
            return [item for item, score in ranking]

    return wrapped_ranking_method


class Election:
    """Given a ballot box, allows you to run social choice methods on the ballot box."""

    def __init__(self, ballot_box: BallotBox):
        self.ballot_box = ballot_box

    ################################################################################################
    # --- Pairwise Methods

    def ranking_by_ranked_pairs(self) -> list:
        matchups = self.ballot_box.get_victory_graph()

        g = nx.DiGraph()
        g.add_nodes_from(matchups.nodes)

        edges = [(u, v, matchups.get_edge_data(u, v)) for (u, v) in matchups.edges]
        edges.sort(key=lambda x: x[2]["margin"], reverse=True)
        for u, v, data in edges:
            g.add_edge(u, v, **data)
            try:
                nx.find_cycle(g)
                g.remove_edge(u, v)
            except nx.NetworkXNoCycle:
                pass

        assert nx.is_directed_acyclic_graph(g)
        return list(nx.topological_sort(g))

    @optional_score
    def ranking_by_copeland(self) -> list:
        g = self.ballot_box.get_victory_graph()
        result = sorted(
            [(n, g.out_degree(n) - g.in_degree(n)) for n in g.nodes],
            key=lambda x: x[1],
            reverse=True,
        )
        return result

    @optional_score
    def ranking_by_minimax(self) -> list:
        g = self.ballot_box.get_matchup_graph()
        return sorted(
            g.nodes, key=lambda n: max(g.get_edge_data(u, v)["margin"] for u, v in g.in_edges(n))
        )

    @optional_score
    def ranking_by_win_ratio(self) -> list:
        matchups = self.ballot_box.get_matchups()

        wins_and_ties_vs_losses = {}
        for candidate in matchups:
            wins_and_ties_vs_losses[candidate] = [0, 0]
            for matchup in matchups[candidate]:
                wins = matchups[candidate][matchup]["wins"]
                losses = matchups[candidate][matchup]["losses"]
                wins_and_ties_vs_losses[candidate][0] += wins
                wins_and_ties_vs_losses[candidate][1] += losses

        ratios = [
            (candidate, (x[0] / ((x[0] + x[1]) or float("inf"))))
            for candidate, x in wins_and_ties_vs_losses.items()
        ]
        return sorted(ratios, key=lambda x: x[1], reverse=True)

    @optional_score
    def ranking_by_win_tie_ratio(self) -> list:
        matchups = self.ballot_box.get_matchups()

        wins_and_ties_vs_losses = {}
        for candidate in matchups:
            wins_and_ties_vs_losses[candidate] = [0, 0]
            for matchup in matchups[candidate]:
                wins = matchups[candidate][matchup]["wins"]
                ties = matchups[candidate][matchup]["ties"]
                losses = matchups[candidate][matchup]["losses"]
                wins_and_ties_vs_losses[candidate][0] += wins + ties
                wins_and_ties_vs_losses[candidate][1] += losses

        ratios = [
            (candidate, (x[0] / ((x[0] + x[1]) or float("inf"))))
            for candidate, x in wins_and_ties_vs_losses.items()
        ]
        return sorted(ratios, key=lambda x: x[1], reverse=True)

    ################################################################################################
    # Ordering based methods

    def supports_ordering_based_methods(self) -> bool:
        return self.ballot_box.supports_ordering_based_methods()

    @optional_score
    def ranking_by_borda_count(self) -> list:
        orderings = self.ballot_box.get_orderings()
        if orderings is None:
            raise ValueError(
                f"Could not retrieve orderings from the ballot box {self.ballot_box}.\n"
                f"Likely, the ballot box was a PairwiseBallotBox. \n"
                f"Use enable_ordering_based_methods to allow this Election to run Borda Count."
            )

        candidates = util.candidates_in_ranked_choice_ballots(orderings)
        # Count the number of candidates each candidate was above, over all ballots
        candidate_wins = {c: 0 for c in candidates}

        for ordering in orderings:
            if len(ordering) == 1:
                continue

            candidates_so_far = ordering[0]
            for more_candidates in ordering[1:]:
                for candidate_already in candidates_so_far:
                    candidate_wins[candidate_already] += len(more_candidates)
                candidates_so_far |= more_candidates

        result = sorted(candidate_wins.items(), key=lambda i: i[1], reverse=True)
        return result

    ################################################################################################
    # Adding support for ordering based methods

    def enable_ordering_based_method(self, intransitivity_resolver, incompleteness_resolver):
        """If this election has a ballot box that supports pairwise comparisons but
        not ordering based methods, use the given intransitivity and incompleteness
        resolver to make each pairwise comparison (or, if there are voters, each voter's
        set of pairwise comparisons) into an ordering.

        :param intransitivity_resolver: see socialchoice.pairwise_collapse.resolving_intransitivity
        :param incompleteness_resolver: see socialchoice.pairwise_collapse.resolving_incompleteness
        :return: None
        """
        self.ballot_box.enable_ordering_based_methods(
            intransitivity_resolver, incompleteness_resolver
        )
