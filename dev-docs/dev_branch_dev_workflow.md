# Typical dev work flow

Assuming you are working on an issue from github:

- Branch from dev to work on one or more issues.
- Code to solve issue.
  - make sure tests, documentation, coverage, etc are passing
- ```scriv create``` to make a changelog fragment.
- make pull request to merge into dev branch, ensure ```closes ###``` as appropriate
- edit scriv fragments to include pr and issue numbers, text details
- ensure local and origin are synced.
- merge working branch into dev
