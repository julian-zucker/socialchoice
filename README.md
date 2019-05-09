
####socialchoice: a library for Social Choice Theory

####Local development
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
```
Now, modifications made in the source will automatically update in your venv, so you can rerun your tests without worrying about if you remembered to re-install the package or not.

