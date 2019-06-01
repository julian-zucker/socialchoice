
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

#### Converting pairwise votes to orderings
Suppose you've collected pairwise votes from several voters, and you want to run a position-based method like [Borda count](https://en.wikipedia.org/wiki/Borda_count). This is easy if each set of pairwise votes is transitive and complete - that is, the voters have consistent preferences (if A is preferred to B, and B is preferred to C, the voter doesn't also prefer C to A) and they have a preference submitted for each candidate pairing. Then, you can [topologically sort](https://en.wikipedia.org/wiki/Topological_sorting) the graph of their votes, and the resulting sorted list of candidates is their ordering. 

But what if the vote set is intransitive or incomplete? If intransitive, you will have cycles, meaning there will be no clear ordering. If incomplete, the output will not contain each candidate. Both make it impossible to run position count directly. However, there are ways of making a vote set transitive, or filling in blanks in an ordering. 

Here is an example of removing an edge from a cycle.
```python
>>> from socialchoice import PairwiseBallotBox, Election   
>>> from socialchoice import IncompletenessResolverFactory
>>> from socialchoice import IntransitivityResolverFactory

>>> ballots = PairwiseBallotBox([(1, 2, "win"), (2, 3, "win"), (3, 1, "win")])
>>> break_random_link = IntransitivityResolverFactory(ballots).make_break_random_link()
>>> add_random_edges = IncompletenessResolverFactory(ballots).make_add_random_edges()

>>> ballots.enable_ordering_based_methods(break_random_link, add_random_edges)
>>> Election(ballots).ranking_by_borda_count() in [[1,2,3], [2,3,1], [3,1,2]]
True
```
As the names imply, this resolves intransitivity by breaking random links, and then ensures that the output is complete by adding random edges. This example resolves an intransitive set of votes (1 beats 2, 2 beats 3, 3 beats 1) to one of the three orderings listed on the last line.