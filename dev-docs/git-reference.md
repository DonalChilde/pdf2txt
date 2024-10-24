# common git commands

```bash
# make a tag
git tag -a v0.0.0 -m "release v0.0.0"
# or
git tag v0.0.0
# tag a previous commit
git tag -a v0.0.1 <commit checksum>
# push a tag to remote
git push origin <tag name>
```

## remove all local branches except master

```bash
#https://coderwall.com/p/x3jmig/remove-all-your-local-git-branches-but-keep-master
git branch | grep -v "master" | xargs git branch -D
```

## rename default branch for new repos

```bash
#https://www.hanselman.com/blog/easily-rename-your-git-default-branch-from-master-to-main
git config --global init.defaultBranch main
```

## dont run hooks

```bash
#https://stackoverflow.com/a/7230886
git commit --no-verify -m "commit message"
```
