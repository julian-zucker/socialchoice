import pytest
from socialchoice import *


@pytest.mark.slow
def test_upsampling_should_be_closer_to_reality():
    """The number of inversions (distance) between the true vote set (pairwise votes)
    and an upsampled collapsed voteset should be less than with a non-upsampled collapsed voteset. In other words,
     we expect upsampling to better reflect reality."""
    import csv

    with open("test/data/dog_project_votes.csv") as votes_fd:
        votes = [x for x in csv.reader(votes_fd)]

    vote_sets = {v[3]: [] for v in votes}

    for vote in votes:
        vote_sets[vote[3]].append(vote[0:3])

    pairwise_ranking = Election(PairwiseBallotBox([vote[0:3] for vote in votes])).ranking_by_ranked_pairs()

    upsampled_votes = pairwise_collapse_by_voter(vote_sets.values(), upsample=True)
    upsampled_ranking = Election(RankedChoiceBallotBox(upsampled_votes)).ranking_by_ranked_pairs()

    votes = pairwise_collapse_by_voter(vote_sets.values(), upsample=False)
    not_upsampled_ranking = Election(RankedChoiceBallotBox(votes)).ranking_by_ranked_pairs()

    assert num_inversions(pairwise_ranking, upsampled_ranking) < num_inversions(pairwise_ranking, not_upsampled_ranking)


