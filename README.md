
#### socialchoice: a library for Social Choice Theory

This library implements [social choice mechanisms](https://en.wikipedia.org/wiki/Social_choice_theory). Development is guided by [this chart](https://en.wikipedia.org/wiki/Ranked_pairs#Comparison_table) with a focus on implementing social choice mechanisms with higher levels of green. 


#### A minimal example
Here, we have two pairwise votes submitted, where `"a"` beat `"b"`, and `"c"` lost to `"b"`. We want to compute the [ranked pairs](https://en.wikipedia.org/wiki/Ranked_pairs) result for this vote set.
```python
>>> from socialchoice import PairwiseBallotBox, Election   
>>> ballots = PairwiseBallotBox([("a", "b", "win"), ("c", "b", "loss")])
>>> election = Election(ballots)
>>> election.ranking_by_ranked_pairs()
['a', 'b', 'c']

```

#### A slightly less minimal example