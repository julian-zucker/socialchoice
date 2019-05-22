#!/usr/bin/env bash

python3 setup.py sdist && \
python3 -m twine upload dist/* --config-file ~/.pypirc -r pypi --verbose  && \
rm -r build/ dist/