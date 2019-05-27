#!/usr/bin/env bash

source venv/bin/activate

rm -r dist/ && \
python3 setup.py sdist && \
python3 -m twine upload dist/* --config-file ~/.pypirc -r pypi --verbose
