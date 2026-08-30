#!/usr/bin/env bash
# Restore teaching Northwind law from git and print harness session wipes.
# Wipe = blank the *agent session*, then re-read law from git.
# Law is not a vector store. This script does not invent policy.
set -euo pipefail

find_root() {
  local dir
  dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  if [[ -f "$dir/AGENTS.md" && -d "$dir/law" ]]; then
    printf '%s\n' "$dir"
    return 0
  fi
  if dir="$(git rev-parse --show-toplevel 2>/dev/null)"; then
    if [[ -f "$dir/AGENTS.md" && -d "$dir/law" ]]; then
      printf '%s\n' "$dir"
      return 0
    fi
  fi
  echo "FAIL: cannot find Openlaw repo root (need AGENTS.md + law/)" >&2
  exit 1
}

ROOT="$(find_root)"
cd "$ROOT"

echo "Openlaw reset-onboarding: $ROOT"
echo "Restoring teaching Northwind law from git (law/, AGENTS.md)."
git checkout -- law/ AGENTS.md

shopt -s nullglob
removed=0
for f in decisions/20*.md; do
  if git ls-files --error-unmatch "$f" >/dev/null 2>&1; then
    continue
  fi
  rm -f "$f"
  echo "removed untracked proposed decision: $f"
  removed=$((removed + 1))
done
shopt -u nullglob
if (( removed == 0 )); then
  echo "no untracked proposed-decision scratch to clear"
fi

echo
echo "Northwind teaching law is on disk. Now wipe the *harness* so the agent is blank:"
cat <<'EOF'

  Herdr / Grok Build
    Start a new pane with cwd = this git repo, or start a new /goal.
    Do not grok --resume an old session if you want a blank agent.

  Cursor Grok Bot
    Start a new Bot thread. Delete Cursor Memories that look like policy.
    Clone this repo into /workspace again if the workspace drifted.

  Hermes
    New session. Leave memory.provider unset. Do not treat MEMORY.md as law
    (remove or ignore it). Re-paste scripts/excerpt-soul.sh into SOUL.md if needed.

  OpenCode
    New session in this directory. Do not load a knowledge-base as policy.

Then read AGENTS.md and law/. If it is not in git, it is not policy.
Optional MCP is a projection of git, not a brain. Re-attach only if the
agent cannot see the working tree (public HTTPS + CANON_MCP_TOKEN; never
commit the token).

  bash scripts/check-law.sh
EOF
echo
echo "reset-onboarding: done"
exit 0
