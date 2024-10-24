# Developer Setup

***NOTE: Assumes Linux OS***

## Existing project with repo

```bash
# get the url to the repository from github.
# from the new project directory...
git clone _repo_url__

# if using pyenv, pick your version if different from global
pyenv shell 3.13
# Setup a virtual environment
python3 -m venv ./.venv
source ./.venv/bin/activate
export PIP_REQUIRE_VIRTUALENV=true
pip3 install -U pip wheel

```

## New project with no existing repo
<!-- dev -->

Assumes default branch name is main, adjust as needed

```bash
# you can set the global default branch
git config --global init.defaultBranch main
```

From the project directory:

```bash
# Setup a virtual environment
# if using pyenv, pick your version
pyenv shell 3.13
python3 -m venv ./.venv
source ./.venv/bin/activate
export PIP_REQUIRE_VIRTUALENV=true
pip3 install -U pip wheel
# Install project dependencies
pip3 install -e .[dev,lint,doc,vscode,testing]
# Create the local git repo, and install git hooks
git init
pre-commit install
pre-commit autoupdate
# Make initial commit. You may have to repeat the add and commit commands if git hooks modify files.
git add .
git commit -m "initial commit"
git tag -a 0.0.0 -m "initial commit tag"
# Link local git repo to a separately created new GitHub project.
git remote add origin https://github.com/DonalChilde/pdf2txt.git
git push -u origin main
git push origin 0.0.0
git branch dev
git push -u origin dev
git checkout dev
```

## Convenient one liners

```bash
# Create the virtual environment and install dependencies

# Pick your python version using pyenv - optional
pyenv shell 3.13

python3 -m venv ./.venv && source ./.venv/bin/activate && export PIP_REQUIRE_VIRTUALENV=true && pip3 install -U pip wheel && pip3 install -e .[dev,lint,doc,vscode,testing]
```

```bash
# Delete and reinstall a virtual environment

# Pick your python version using pyenv - optional
pyenv shell 3.13

rm -rf ./.venv && python3 -m venv ./.venv && source ./.venv/bin/activate && export PIP_REQUIRE_VIRTUALENV=true && pip3 install -U pip wheel && pip3 install -e .[dev,lint,doc,vscode,testing]
```

```bash
# Create the local git repo, and install git hooks
git init && pre-commit install && pre-commit autoupdate
```

```bash
# Make initial commit. You may have to repeat this command if git hooks modify files
git add . && git commit -m "initial commit" && git tag -a 0.0.0 -m "initial commit tag"
```

```bash
# Link a new local git repo to a separately created new GitHub project.
git remote add origin https://github.com/DonalChilde/pdf2txt.git && git push -u origin main && git push origin 0.0.0 && git branch dev && git push -u origin dev && git checkout dev
```

### GitHub setup

- Project->settings->Actions-> allow actions read/write access
- Actions->Labeler_manual-> manually run workflow one time to establish Labels.

<!-- end-dev -->
