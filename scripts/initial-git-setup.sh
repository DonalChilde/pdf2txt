#!/usr/bin/env bash

# Run from the project directory
# this is only ment to be run on a new project

# Create the local git repo, and install git hooks
git init --initial-branch=main
./.venv/bin/pre-commit install
./.venv/bin/pre-commit autoupdate
./.venv/bin/pre-commit run --all-files

# run these before the git hooks to try to avoid
# having the first commit fail
# ./.venv/bin/black ./src ./tests .
# ./.venv/bin/isort ./src ./tests .

# Make initial commit. You may have to repeat the add and commit commands if git hooks modify files.
git add .
git commit -m "initial commit"
git tag -a 0.0.0 -m "initial commit tag"
