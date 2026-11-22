#!/usr/bin/env bash
# Animation Studio — AUTOSAVE (Claude Code Stop hook, project setting).
# Director (22 Nov): "aane wale sab kaam apne aap save hona chahiye, kuch bhi gumna nahi chahiye".
# Every time Claude finishes a reply, for EACH project repo (main `animation-studio` + the sibling `animation-studio-scenes`
# if it is checked out next to it): if it has changes → git add -A → commit "autosave: …" → push the CURRENT branch.
# Safety: current branch only, never force-push; skipped during merge / rebase / cherry-pick and on a detached HEAD;
# files > 95 MB (GitHub hard limit 100 MB) are left out and reported; files > 50 MB are committed but WARNED (GitHub warns);
# repo (.git) > 5 GB → warning (Director: storage plan = new repo per stage); push retried 4× with back-off; if the remote branch
# moved, it is merged (no rebase, no force) and pushed again; on conflict the merge is aborted and reported. Never blocks (exit 0).
set -u
exec 2>>/tmp/autosave_hook.log          # keep git's progress / negotiation noise out of Claude's hook output
ROOT="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null)}"
MSGS=()
note() { MSGS+=("$1"); }

save_repo() {   # $1 = repo dir
  local D="$1" NAME BR GD f N TOP SESS SHA BIG BIGW size kb
  cd "$D" 2>/dev/null || return 0
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || return 0
  NAME=$(basename "$D")
  BR=$(git symbolic-ref --quiet --short HEAD) || { note "$NAME: autosave skipped (detached HEAD)."; return 0; }
  GD=$(git rev-parse --git-dir)
  for f in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD; do
    [ -e "$GD/$f" ] && { note "$NAME: autosave skipped (git $f in progress)."; return 0; }
  done
  [ -z "$(git status --porcelain)" ] && return 0                       # nothing changed → silent
  git add -A
  BIG=(); BIGW=()
  while IFS= read -r -d '' f; do
    [ -f "$f" ] || continue
    size=$(stat -c %s "$f" 2>/dev/null || echo 0)
    if [ "$size" -gt 95000000 ]; then BIG+=("$f"); elif [ "$size" -gt 50000000 ]; then BIGW+=("$f"); fi
  done < <(git diff --cached --name-only -z --diff-filter=AM)
  for f in "${BIG[@]}"; do git reset -q -- "$f"; done
  if git diff --cached --quiet; then
    [ ${#BIG[@]} -gt 0 ] && note "$NAME: only files > 95 MB changed — NOT pushed (GitHub limit): ${BIG[*]}"
    return 0
  fi
  N=$(git diff --cached --name-only | wc -l)
  TOP=$(git diff --cached --name-only | awk -F/ '{print (NF > 2 ? $1"/"$2 : $1)}' | sort | uniq -c | sort -rn | head -3 | awk '{print $2}' | paste -sd ', ' -)
  SESS=""; [ -n "${CLAUDE_CODE_REMOTE_SESSION_ID:-}" ] && SESS="Claude-Session: https://claude.ai/code/session_${CLAUDE_CODE_REMOTE_SESSION_ID#cse_}"
  git commit -q -m "autosave: $(date -u '+%Y-%m-%d %H:%M UTC') · $N files · $TOP" -m "Automatic save by the project Stop hook (animation-studio/.claude/hooks/autosave.sh)." \
    -m "Co-Authored-By: Claude <noreply@anthropic.com>${SESS:+
$SESS}" || { note "$NAME: commit failed — changes are still in the working tree."; return 0; }
  SHA=$(git rev-parse --short HEAD)
  pushit() { for i in 1 2 3 4; do git -c push.negotiate=true push -q -u origin "$BR" 2>/tmp/autosave_push.err && return 0; sleep $((2 ** i)); done; return 1; }
  if ! pushit; then
    if git fetch -q origin "$BR" 2>/dev/null && git merge -q --no-edit FETCH_HEAD 2>/dev/null; then
      pushit || { note "$NAME: committed $SHA locally, push FAILED ($(tail -1 /tmp/autosave_push.err)). Next stop retries."; return 0; }
    else
      git merge --abort 2>/dev/null
      note "$NAME: committed $SHA locally; remote branch has conflicting changes — not pushed. Needs a manual merge."
      return 0
    fi
  fi
  SHA=$(git rev-parse --short HEAD)
  local m="$NAME: $N files committed + pushed ($BR @ $SHA)."
  [ ${#BIG[@]} -gt 0 ] && m="$m Left out (> 95 MB, GitHub limit): ${BIG[*]}"
  [ ${#BIGW[@]} -gt 0 ] && m="$m WARNING files > 50 MB (GitHub warns, repo grows fast): ${BIGW[*]}"
  kb=$(du -sk "$GD" 2>/dev/null | cut -f1)
  [ "${kb:-0}" -gt 5000000 ] && m="$m WARNING: .git is $((kb / 1000000)) GB (> 5 GB) — tell the Director (storage plan: new repo per stage)."
  note "$m"
}

[ -n "$ROOT" ] || exit 0
save_repo "$ROOT"
SIB="$(dirname "$ROOT")/animation-studio-scenes"
[ -d "$SIB/.git" ] && save_repo "$SIB"
if [ ${#MSGS[@]} -gt 0 ]; then
  printf '{"systemMessage": %s}\n' "$(printf '%s ' "${MSGS[@]}" | jq -Rs .)"
fi
exit 0
