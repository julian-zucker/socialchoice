
#### socialchoice: a library for Social Choice Theory

This library implements [social choice mechanisms](https://en.wikipedia.org/wiki/Social_choice_theory).

#### Install
socialchoice is on PyPI, so:
``` 
pip3 install socialchoice
```

#### A minimal example
Here, we have two pairwise votes submitted, where `"a"` beat `"b"`, and `"c"` lost to `"b"`. We want to compute the [ranked pairs](https://en.wikipedia.org/wiki/Ranked_pairs) result for this vote set.
```python
>>> from socialchoice import PairwiseBallotBox, Election   
>>> pairwise_ballots = PairwiseBallotBox([("a", "b", "win"), ("c", "b", "loss")])
>>> election = Election(pairwise_ballots)
>>> election.ranking_by_ranked_pairs()
['a', 'b', 'c']

```

#### A slightly less minimal example
Let's run a ranked choice election, using ranked pairs again.
```python
>>> from socialchoice import RankedChoiceBallotBox, Election   
>>> ranked_ballots = RankedChoiceBallotBox([[1,2,3,4], [1, {2,3}, 4]])
>>> election = Election(ranked_ballots)
>>> election.ranking_by_ranked_pairs()
[1, 2, 3, 4]

```
Notice that ties are allowed - simply submit a set as one element of your ranking, and each of those will be counted as ties. Ranked choice ballots are converted into pairwise preferences, and then ranked pairs can be run on the result.