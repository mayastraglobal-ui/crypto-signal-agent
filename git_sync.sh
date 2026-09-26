#!/usr/bin/env bash
# The Save steps' `git pull --rebase` (scan.yml, research.yml): bring this run's commit on top of the newest main.
#
# Two runs can start from the same main (GitHub checks out the commit a run was queued for, so a scan queued behind
# another scan starts from the older main). Their generated files under reports/ (latest.md, positions.json ...)
# then clash. Those files are rebuilt by every run, so THIS run's copies win. A clash anywhere else stops the run
# and nothing is pushed. The append-only files keep their own merge driver (append_merge.py), and the workflow still
# runs `memory_guard.py --after-sync` after this, before `git push`.
#
#   bash git_sync.sh            (exit 0 = rebased on the newest main; 1 = a clash outside reports/, nothing changed)
set -u

in_rebase() { [ -d "$(git rev-parse --git-path rebase-merge)" ] || [ -d "$(git rev-parse --git-path rebase-apply)" ]; }

if git pull --rebase --autostash; then
  exit 0
fi
for _ in 1 2 3 4 5 6 7 8 9 10; do
  in_rebase || break
  files=$(git diff --name-only --diff-filter=U)
  if [ -z "$files" ] || printf '%s\n' "$files" | grep -qv '^reports/'; then
    echo "git_sync: a clash outside reports/ - nothing is pushed:"
    printf '  %s\n' $files
    git rebase --abort
    exit 1
  fi
  echo "git_sync: generated reports clashed with a newer run - this run's copies win:"
  printf '%s\n' "$files" | while IFS= read -r f; do
    echo "  $f"
    if git checkout --theirs -- "$f" 2>/dev/null; then git add -- "$f"; else git rm -q -- "$f"; fi
  done
  GIT_EDITOR=true git rebase --continue >/dev/null 2>&1 || true
done
if in_rebase; then
  echo "git_sync: the rebase did not finish - nothing is pushed"
  git rebase --abort
  exit 1
fi
exit 0
