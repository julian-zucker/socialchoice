#!/usr/bin/env bash
set -e

source ./venv/bin/activate

rm -rf dist/
python3 setup.py sdist
python3 -m twine upload dist/* --config-file ~/.pypirc -r pypi --verbose
