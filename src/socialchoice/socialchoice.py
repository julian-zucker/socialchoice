import networkx

class Election:
    """
    A user adds votes to the election and can retrieve results from the election.
    """

    def __init__(self, *votes):
        """
        :param votes: An array of votes, where a vote is any indexable object of length 3
                Each vote looks like this: ["Alice",  "Bob", "won"] which indicates that "Alice" lost to "Bob".
        """
        assert are_valid_votes(votes)
        self._votes = list(votes)
        self._candidates = get_all_candidates_from_votes(self._votes)

    def add_votes(self, *votes) -> None:
        assert are_valid_votes(votes)
        self._votes += votes
        self._candidates |= get_all_candidates_from_votes(votes)

    def get_votes(self) -> list:
        return self._votes.copy()

    def get_candidates(self) -> set:
        return self._candidates.copy()

    def get_victory_graph(self) -> networkx.DiGraph:
        """
        :return: Every out-edge is a loss to another candidate, every in-edge is a win
        """
        matchups = self.get_matchup_graph()
        edges_to_remove = []
        for u, v in matchups.edges:
            margin_u_to_v = matchups.get_edge_data(u, v)["margin"]
            margin_v_to_u = matchups.get_edge_data(v, u)["margin"]

            # u->v has higher win margin than v->u, keep lower margin
            if margin_u_to_v <= margin_v_to_u:
                edges_to_remove.append((u, v))

        matchups.remove_edges_from(edges_to_remove)
        return matchups

    def get_matchup_graph(self) -> networkx.DiGraph:
        """
        :return: fully connected graph
        """
        matchups = self.get_matchups()
        ids = matchups.keys()

        g = networkx.DiGraph()
        g.add_nodes_from(ids)
        for candidate1 in matchups:
            for candidate2 in matchups[candidate1]:
                candidate1to2 = matchups[candidate1][candidate2]
                total_votes_candidate1to2 = sum(candidate1to2.values())
                if total_votes_candidate1to2 != 0:
                    g.add_edge(candidate1, candidate2,
                               wins=candidate1to2["wins"],
                               losses=candidate1to2["losses"],
                               ties=candidate1to2["ties"],
                               margin=candidate1to2["wins"] / total_votes_candidate1to2)

                candidate2to1 = matchups[candidate2][candidate1]
                total_votes_candidate2to1 = sum(candidate2to1.values())
                if total_votes_candidate2to1 != 0:
                    g.add_edge(candidate2, candidate1,
                               wins=candidate2to1["wins"],
                               losses=candidate2to1["losses"],
                               ties=candidate2to1["ties"],
                               margin=candidate2to1["wins"] / total_votes_candidate2to1)

        return g


    def get_matchups(self) -> dict:
        """
        :return: Mapping from candidate to a mapping from the candidates they have played to their "win" "losses" "ties"
        """
        matchups = {} # A matrix so we can have all the
        for candidate in self._candidates:
            matchups[candidate] = {}
        for candidate1 in self._candidates:
            for candidate2 in self._candidates:
                if candidate1 == candidate2:
                    continue
                matchups[candidate1][candidate2] = {"wins": 0, "losses": 0, "ties": 0}
                matchups[candidate2][candidate1] = {"wins": 0, "losses": 0, "ties": 0}

        for vote in self._votes:
            candidate1, candidate2, result = vote
            if result == "win":
                matchups[candidate1][candidate2]["wins"] += 1
                matchups[candidate2][candidate1]["losses"] += 1
            if result == "loss":
                matchups[candidate1][candidate2]["losses"] += 1
                matchups[candidate2][candidate1]["wins"] += 1
            if result == "tie":
                matchups[candidate1][candidate2]["ties"] += 1
                matchups[candidate2][candidate1]["ties"] += 1

        return matchups

    def get_ranked_pairs_ranking(self) -> list:
        matchups = self.get_victory_graph()

        g = networkx.DiGraph()
        g.add_nodes_from(matchups.nodes)

        edges = [(u, v, matchups.get_edge_data(u, v)) for (u, v) in matchups.edges]
        edges.sort(key=lambda x: x[2]["margin"], reverse=True)
        for u, v, data in edges:
            g.add_edge(u, v, **data)
            try:
                networkx.find_cycle(g)
                g.remove_edge(u, v)
            except networkx.NetworkXNoCycle:
                pass

        assert networkx.is_directed_acyclic_graph(g)
        return list(networkx.topological_sort(g))


    def ranked_pairs(self) -> list:
        matchups = self.get_victory_graph()

        g = networkx.DiGraph()
        g.add_nodes_from(matchups.nodes)

        edges = [(u, v, matchups.get_edge_data(u, v)) for (u, v) in matchups.edges]
        edges.sort(key=lambda x: x[2]["margin"], reverse=True)
        for u, v, data in edges:
            g.add_edge(u, v, **data)
            try:
                networkx.find_cycle(g)
                g.remove_edge(u, v)
            except networkx.NetworkXNoCycle:
                pass

        assert networkx.is_directed_acyclic_graph(g)
        return list(networkx.topological_sort(g))

    def get_copeland(self) -> list:
        g = self.get_victory_graph()
        return sorted([(n, g.out_degree(n) - g.in_degree(n)) for n in g.nodes], key=lambda x: x[1], reverse=True)

    def get_minimax(self) -> list:
        g = self.get_matchup_graph()
        return sorted(g.nodes, key=lambda n: max(g.get_edge_data(u, v)["margin"] for u, v in g.in_edges(n)))

    def get_win_ratio(self) -> list:
        matchups = self.get_matchups()

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

    def get_win_tie_ratio(self) -> list:
        matchups = self.get_matchups()

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


def get_all_candidates_from_votes(votes) -> set:
    """
    :return: All the candidates mentioned in the votes
    """
    return {vote[0] for vote in votes} | {vote[1] for vote in votes}

def are_valid_votes(votes: iter) -> bool:
    return all(vote[2] in {"win", "loss", "tie"} for vote in votes)
