#!/usr/bin/env bash

[ -e .tox/cookie/bin/activate ] || tox -e cookie
source .tox/cookie/bin/activate
cookiecutter_code/rock-init.py $@
