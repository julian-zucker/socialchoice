import functools

import networkx as nx

from ballot import BallotBox


def optional_score(ranking_method):
    """Adds a flag to include or remove the score from a ranking method that returns a list of 2-tuples,
    where the first element is the candidate, and the second element is a score.

    :param ranking_method: a method on an Election
    :return: the same ranking method, but with a flag `include_score`, which defaults to False. If set to true, the
    function returns a list of 2-tuples instead of just a ranking
    """
    # This unfortunately has to be defined above Election to be used in Election

    @functools.wraps(ranking_method)
    def wrapped_ranking_method(self, include_score=False):
        if include_score:
            return ranking_method(self)
        else:
            return [item for item, score in ranking_method(self)]

    return wrapped_ranking_method


class Election:
    """Given a ballot box, allows you to run social choice methods on the ballot box."""

    def __init__(self, ballot_box: BallotBox):
        self.ballot_box = ballot_box

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
        result = sorted([(n, g.out_degree(n) - g.in_degree(n)) for n in g.nodes], key=lambda x: x[1], reverse=True)
        return result

    @optional_score
    def ranking_by_minimax(self) -> list:
        g = self.ballot_box.get_matchup_graph()
        return sorted(g.nodes, key=lambda n: max(g.get_edge_data(u, v)["margin"] for u, v in g.in_edges(n)))

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

        ratios = [(candidate, (x[0] / ((x[0] + x[1]) or float("inf"))))
                  for candidate, x in wins_and_ties_vs_losses.items()]
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

        ratios = [(candidate, (x[0] / ((x[0] + x[1]) or float("inf"))))
                  for candidate, x in wins_and_ties_vs_losses.items()]
        return sorted(ratios, key=lambda x: x[1], reverse=True)
