#!/usr/bin/env bash

# Run from the project directory

# Setup a virtual environment
# if using pyenv, pick your version
pyenv shell 3.13

if [ -d ./.venv ]; then
    echo "Removing venv at ./.venv"
    rm -rf ./.venv
fi

python3 -m venv ./.venv
# source ./.venv/bin/activate
# export PIP_REQUIRE_VIRTUALENV=true
./.venv/bin/pip install -U pip wheel
# Install project dependencies
./.venv/bin/pip install -e .[dev,lint,doc,vscode,testing]
