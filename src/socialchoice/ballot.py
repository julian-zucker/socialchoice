import networkx as nx

from pairwise_collapse import pairwise_collapse


class BallotBox:
    """An interface for the features of ballot boxes"""

    def get_victory_graph(self) -> nx.DiGraph:
        """A victory graph is a matchup graph of each candidate, but with only edges for wins. Every out-edge represents
         a win over another candidate. Two candidates will not have any edge between them if there is a perfect tie by
         win ratio.

        See `get_matchup_graph` for a description of the attributes on nodes and edges.
         """
        pass

    def get_matchup_graph(self) -> nx.DiGraph:
        """A matchup graph is a fully-connected graph, with each out-edge corresponding to a matchup and each in-edge
        corresponding to the same matchup, but with wins and losses flipped. An edge `(a, b)` from a to b will have
        `wins` corresponding to the number of wins `a` has over `b`, while the edge `(b, a)` will have `wins`
        corresponding to the number of wins `b` has over `a`.

        Every edge has the attributes `wins` (described above), `losses`, `ties`, and `margin`. `losses` and `ties` are
        self explanatory, simply the number of losses or ties between the two candidates. `margin` is the ratio of
        wins to overall votes.
        """
        pass

    def get_matchups(self) -> dict:
        """This matchup shows the number of wins and losses each candidate has against each other.
        The shape of the final dictionary returned is:

         >>> {\
            "candidate1": { \
                 {"candidate2": {"win": 12, "loss": 10, "tie": 5}}, \
                 {"candidate3": {"win": 3,  "loss": 23, "tie": 9}}, \
                 # potentially many more \
             }, \
             "candidate2": { \
                 {"candidate1": {"win": 10, "loss": 12, "tie": 5}}, \
                 {"candidate3": {"win": 23, "loss":  3, "tie": 9}}, \
                 # potentially many more \
             },\
             # and so on\
          }

        :return: a matchup mapping, as described above
        """


class PairwiseBallotBox(BallotBox):
    """Stores ballots in pairwise form, as in: ["Alice",  "Bob", "win"]"""

    def __init__(self, votes, candidates=None):
        """
        Creates a new pairwise Ballot.

        :param votes: An array of votes, where a vote is any indexable object of length 3
        :param candidates: None, meaning to infer the candidate set from the votes, or a collection of the candidates
                           that were being voted on in this election.
        :raises InvalidVoteShapeException: if given any vote with length != 3
        """
        self.ballots = self.__ensure_valid_votes(votes)
        self.candidates = candidates or self.__get_all_candidates_from_votes(self.ballots)

    @staticmethod
    def __get_all_candidates_from_votes(votes) -> set:
        """
        :return: All the candidates mentioned in the votes
        """
        return {vote[0] for vote in votes} | {vote[1] for vote in votes}

    @staticmethod
    def __ensure_valid_votes(votes: iter) -> list:
        for vote in votes:
            if not len(vote) == 3:
                raise InvalidBallotDataException("Expected a vote of length three, got " + str(vote))

            if not vote[2] in {"win", "loss", "tie"}:
                raise InvalidBallotDataException(
                    """Expected type to be one of {"win", "loss", "tie"}, got""" + str(vote))

        return list(votes)

    def get_victory_graph(self) -> nx.DiGraph:
        matchups = self.get_matchup_graph()
        edges_to_remove = []
        for u, v in matchups.edges:
            margin_u_to_v = matchups.get_edge_data(u, v)["margin"]
            margin_v_to_u = matchups.get_edge_data(v, u)["margin"]

            # u->v has lower win margin than v->u, keep the "winning edge" with higher win ratio
            # this will remove both if there is a perfect tie - but that's okay
            if margin_u_to_v <= margin_v_to_u:
                edges_to_remove.append((u, v))

        matchups.remove_edges_from(edges_to_remove)
        return matchups

    def get_matchup_graph(self) -> nx.DiGraph:
        matchups = self.get_matchups()
        ids = matchups.keys()

        g = nx.DiGraph()
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
        matchups = {}
        for candidate in self.candidates:
            matchups[candidate] = {}
        for candidate1 in self.candidates:
            for candidate2 in self.candidates:
                if candidate1 == candidate2:
                    continue
                matchups[candidate1][candidate2] = {"wins": 0, "losses": 0, "ties": 0}
                matchups[candidate2][candidate1] = {"wins": 0, "losses": 0, "ties": 0}

        for vote in self.ballots:
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

    def to_ranked_choice_ballot_box(self):
        return RankedChoiceBallotBox(pairwise_collapse(self.ballots))



class RankedChoiceBallotBox(BallotBox):
    def __init__(self, ballots, candidates=None, require_full_ballots=False):
        self.ballots = self.__ensure_valid_ballots(ballots, candidates, require_full_ballots)

        pairwise_ballots = []

        for ranking in ballots:
            for i, candidate in enumerate(ranking):
                for candidate2 in ranking[i + 1:]:
                    pairwise_ballots.append((candidate, candidate2, "win"))

        self.pairwise_ballot_box = PairwiseBallotBox(pairwise_ballots)

    def get_victory_graph(self) -> nx.DiGraph:
        return self.pairwise_ballot_box.get_victory_graph()

    def get_matchup_graph(self) -> nx.DiGraph:
        return self.pairwise_ballot_box.get_matchup_graph()

    def get_matchups(self) -> dict:
        return self.pairwise_ballot_box.get_matchups()

    def __ensure_valid_ballots(self, ballots, candidates, require_full_ballots):
        if len(ballots) == 0 or any(not isinstance(ballot, list) for ballot in ballots):
            raise InvalidBallotDataException("Ballots must be a non-empty iterable of lists")

        def ballot_candidates(ballot):
            """Gets the set of candidates written in a a ballot.
            This is slightly involved because a ranking with ties contains elements that are either a non-list
            element (a single candidate) or a list, which is a set of candidates that are tied. Simple flattening
            doesn't work, you have to check every element for list-ness, but only once because it can't be nested.
            """
            candidate_set = set()
            for item in ballot:
                if isinstance(item, list):
                    # If there is a list, it is a tie, so process it one element at a time.
                     for elem in item:
                        if elem in candidate_set:
                            raise InvalidBallotDataException(f"Candidate {elem} appears multiple times in{ballot}")
                        candidate_set.add(elem)
                else:
                    # If it's not a list, we can just process one at a time.
                    if item in candidate_set:
                        raise InvalidBallotDataException(f"Candidate {item} appears multiple times in{ballot}")
                    candidate_set.add(item)
            return candidate_set

        # Need to either get or infer the candidate set to validate that ballots are full, and to ensure that each
        # ballot doesn't contain elements not in the candidate set.
        if candidates:
            candidate_set = set(candidates)
            if not len(candidates) == len(candidate_set):
                raise InvalidElectionDataException(f"Duplicate candidates in {candidates}")
        else:
            candidate_set = set()
            for ballot in ballots:
                candidate_set |= ballot_candidates(ballot)

        for ballot in ballots:
            ballot_contents = ballot_candidates(ballot)

            for vote_candidate in ballot_contents:
                if vote_candidate not in candidate_set:
                    raise InvalidBallotDataException(f"Ballot {ballot} contains candidate {vote_candidate}, " +
                                                     f"which is not found in candidate set {candidate_set}")

            if require_full_ballots:
                if ballot_contents != candidate_set:
                    raise InvalidBallotDataException(f"Requiring full ballots: ballot {ballot}" +
                                                     f" did not contain all of {candidate_set}.")

        return ballots


class InvalidElectionDataException(Exception):
    """Raised if there is invalid data somewhere other than the ballots."""


class InvalidBallotDataException(Exception):
    """Raised if a ballot has invalid data, for example, contains a candidate not in the list of candidates."""
