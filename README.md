
#### socialchoice: a library for Social Choice Theory

This library implements [social choice mechanisms](https://en.wikipedia.org/wiki/Social_choice_theory). The design goal is to have a consistent API for working with votes, and provide efficient algorithms for computing both social choice mechanisms and answering questions about the vote data. Development is guided by [this chart](https://en.wikipedia.org/wiki/Ranked_pairs#Comparison_table) with a focus on implementing social choice mechanisms with higher levels of green. 


#### A minimal example
Here, we have two pairwise votes submitted, where `"a"` beat `"b"`, and `"c"` lost to `"b"`. We want to compute the [ranked pairs](https://en.wikipedia.org/wiki/Ranked_pairs) result for this vote set.
```python
>>> from socialchoice import PairwiseBallotBox, Election   
>>> ballots = PairwiseBallotBox([("a", "b", "win"), ("c", "b", "loss")])
>>> election = Election(ballots)
>>> election.ranking_by_ranked_pairs()
['a', 'b', 'c']

```


#### Local development
First, setup a virtual environment and install a local version of the package.
```bash
# Run this from the top level directory
virtualenv -p python3.7 venv
source ./venv/bin/activate

pip3 install -e src/socialchoice/
pip3 install -r requirements.txt
```
Now, modifications made in the source will automatically update in your venv, so you can rerun your tests without worrying about if you remembered to re-install the package or not. Run the tests, just to be sure:
```bash
py.test --doctest-glob=*.md
```


