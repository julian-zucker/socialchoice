import networkx as nx

from ballot import BallotBox


class Election:
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

    def ranking_by_copeland(self) -> list:
        g = self.ballot_box.get_victory_graph()
        return sorted([(n, g.out_degree(n) - g.in_degree(n)) for n in g.nodes], key=lambda x: x[1], reverse=True)

    def ranking_by_minimax(self) -> list:
        g = self.ballot_box.get_matchup_graph()
        return sorted(g.nodes, key=lambda n: max(g.get_edge_data(u, v)["margin"] for u, v in g.in_edges(n)))

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
