# Release Workflow

Before a release, ensure all of the following are completed.

- [ ] Ensure all changes committed and synced!
- [ ] All tests pass!
- [ ] Coverage is acceptable.
- [ ] Documentation is current.
- [ ] make a release branch from dev -> 'release-0.0.0'
- [ ] Update ```__init__.py.__version__``` with new version number.
- [ ] Check scriv fragments for completion.
- [ ] ```scriv collect``` to update changelog.
- [ ] Edit changelog.
- [ ] Make a PR on github to merge the release branch with main
- [ ] Merge the PR
- [ ] Checkout main branch
- [ ] Tag the new version on the main branch
- [ ] Push the tag to origin
- [ ] Create release from Draft Release on github
  - [ ] Ensure correct tag and version are used.
  - [ ] Update release notes as necessary, can copy paste from changelog.
- [ ] Update the dev branch from main

```bash
# Make a release branch from the dev branch
git checkout -b release-0.0.0
git push -u origin release-0.0.0

# Tag the release version on the main branch
git tag -a 0.0.0 -m "release 0.0.0"
git push origin v0.0.0
```
