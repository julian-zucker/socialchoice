### Contributing
This file explains how to contribute to `socialchoice`. As the library is not yet on PyPI, we have
no CI system, and there is only one contributor, I'm committing straight to master. This will
change once a v1 is launched.

----------------------------------------------------------------------------------------------------
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
py.test --doctest-glob=*.md --strict -k "not slow"
```

----------------------------------------------------------------------------------------------------
#### Testing
Run all tests with `py.test --doctest-glob *.md --strict`, and run only the fast tests with `py.test --doctest-glob *.md --strict -k "not slow"`. I chose to mark only the slow tests, and not mark each fast test with `@pytest.mark.fast`, as fast unit tests are the default.
##### Tags/Markers
You can find the list of test tags in [`pytest.ini`](pytest.ini). Running pytest with --strict will error if a tag not listed under `markers` is used to mark a test.

For testing, `socialchoice` uses both standard, example-based tests, and property-based tests through [hypothesis](https://hypothesis.works). The general testing strategy is to write enough example-based tests that you are confident your code works on normal cases, and then add property-based tests as an explanation of what properties your code has.
 