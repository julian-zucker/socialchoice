
####socialchoice: a library for Social Choice Theory

This library implements [social choice mechanisms](https://en.wikipedia.org/wiki/Social_choice_theory) with a consistent API. Development is guided by [this chart](https://en.wikipedia.org/wiki/Ranked_pairs#Comparison_table) with a focus on implementing social choice mechanisms that are more green than red. 


#### A minimal example
```
>>> from socialchoice import PairwiseBallets, Election   
>>> ballots = PairwiseBallets([("scala", "python3", "win"), ("java", "python3", "loss")])
>>> election = Election(ballots)
>>> election.ranking_by_ranked_pairs()
['scala', 'python3', 'java']

```


#### Local development
First, setup a virtual environment and install a local version of the package.
```bash
# Run this from the top level directory, one level above src and test
virtualenv -p python3.7 venv
source ./venv/bin/activate

pip3 install -e src/socialchoice/
pip3 install -r requirements.txt
```
Run the tests, just to be sure:
```bash
py.test test/
python3 -m doctest -v README.md
```
Now, modifications made in the source will automatically update in your venv, so you can rerun your tests without worrying about if you remembered to re-install the package or not.

