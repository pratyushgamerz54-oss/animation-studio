#!/usr/bin/env bash
# Animation Studio — AUTOSAVE (Claude Code Stop hook, project setting).
# Director (22 Nov): "aane wale sab kaam apne aap save hona chahiye, kuch bhi gumna nahi chahiye".
# Every time Claude finishes a reply: if the project has changes → git add -A → commit "autosave: …" → push the CURRENT branch.
# Safety: current branch only, never force-push; skipped during merge / rebase / cherry-pick and on a detached HEAD;
# files > 95 MB (GitHub hard limit 100 MB) are left out and reported; push retried 4× with back-off; if the remote branch moved,
# it is merged (no rebase, no force) and pushed again; on conflict the merge is aborted and reported. Never blocks Claude (exit 0).
set -u
ROOT="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null)}"
cd "$ROOT" 2>/dev/null || exit 0
say() { printf '{"systemMessage": %s}\n' "$(printf '%s' "$1" | jq -Rs .)"; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
BR=$(git symbolic-ref --quiet --short HEAD) || { say "Autosave skipped: detached HEAD (no branch to push)."; exit 0; }
GD=$(git rev-parse --git-dir)
for f in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD; do
  [ -e "$GD/$f" ] && { say "Autosave skipped: git $f in progress."; exit 0; }
done
[ -z "$(git status --porcelain)" ] && exit 0                         # nothing changed → silent
# ---------------------------------------------------------------- stage everything except files GitHub would reject
git add -A
BIG=()
while IFS= read -r -d '' f; do
  [ -f "$f" ] && [ "$(stat -c %s "$f" 2>/dev/null || echo 0)" -gt 95000000 ] && BIG+=("$f")
done < <(git diff --cached --name-only -z --diff-filter=AM)
for f in "${BIG[@]}"; do git reset -q -- "$f"; done
if git diff --cached --quiet; then
  [ ${#BIG[@]} -gt 0 ] && say "Autosave: only files > 95 MB changed — NOT pushed (GitHub limit): ${BIG[*]}"
  exit 0
fi
N=$(git diff --cached --name-only | wc -l)
TOP=$(git diff --cached --name-only | awk -F/ '{print (NF > 2 ? $1"/"$2 : $1)}' | sort | uniq -c | sort -rn | head -3 | awk '{print $2}' | paste -sd ', ' -)
SESS=""; [ -n "${CLAUDE_CODE_REMOTE_SESSION_ID:-}" ] && SESS="Claude-Session: https://claude.ai/code/session_${CLAUDE_CODE_REMOTE_SESSION_ID#cse_}"
git commit -q -m "autosave: $(date -u '+%Y-%m-%d %H:%M UTC') · $N files · $TOP" -m "Automatic save by the project Stop hook (.claude/hooks/autosave.sh)." \
  -m "Co-Authored-By: Claude <noreply@anthropic.com>${SESS:+
$SESS}" || { say "Autosave: commit failed — changes are still in the working tree."; exit 0; }
SHA=$(git rev-parse --short HEAD)
# ---------------------------------------------------------------- push (retry, merge if the remote moved — never force)
push() { for i in 1 2 3 4; do git push -q -u origin "$BR" 2>/tmp/autosave_push.err && return 0; sleep $((2 ** i)); done; return 1; }
if ! push; then
  if git fetch -q origin "$BR" 2>/dev/null && git merge -q --no-edit FETCH_HEAD 2>/dev/null; then
    push || { say "Autosave: committed $SHA locally, push FAILED ($(tail -1 /tmp/autosave_push.err)). Next stop retries."; exit 0; }
  else
    git merge --abort 2>/dev/null
    say "Autosave: committed $SHA locally; remote branch has other changes that conflict — not pushed. Needs a manual merge."
    exit 0
  fi
fi
SHA=$(git rev-parse --short HEAD)                                     # after a merge this is the merge commit
MSG="Autosave: $N files committed + pushed ($BR @ $SHA)."
[ ${#BIG[@]} -gt 0 ] && MSG="$MSG Left out (> 95 MB, GitHub limit): ${BIG[*]}"
say "$MSG"
exit 0
