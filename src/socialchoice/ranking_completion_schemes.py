"""Functions that will add missing items into a partial ranking."""
import random


def fill_uniformly(partial_ranking, to_add):
    for item in to_add:
        partial_ranking.insert(random.randint(1, max(1, len(partial_ranking) - 1)), item)
    return partial_ranking


def fill_by_average_rank_in_completes(vote_set):
    def filler(partial_ranking, to_add):
        return partial_ranking

    return filler


def fill_by_elo(vote_set):
    def filler(partial_ranking, to_add):
        return partial_ranking

    return filler
