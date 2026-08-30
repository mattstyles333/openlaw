#!/usr/bin/env bash
# Copy decisions/_template.md into a new proposed ADR and print next steps.
# Offline. No secrets. Does not write law/ or AGENTS.md. Does not merge.
set -euo pipefail

usage() {
  echo "Usage: bash scripts/propose.sh [slug]" >&2
  echo "Writes decisions/proposed/YYYY-MM-DD-<slug>.md from decisions/_template.md" >&2
}

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

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi
if [[ $# -gt 1 ]]; then
  usage
  exit 1
fi

ROOT="$(find_root)"
cd "$ROOT"

TEMPLATE="$ROOT/decisions/_template.md"
DEST_DIR="$ROOT/decisions/proposed"

if [[ ! -f "$TEMPLATE" ]]; then
  echo "FAIL: missing template $TEMPLATE" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

DATE="$(date -u +%Y-%m-%d)"
raw="${1:-proposal}"
# Slug is a filename suffix, never a path.
SLUG="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9-' '-')"
SLUG="${SLUG#-}"
SLUG="${SLUG%-}"
if [[ -z "$SLUG" ]]; then
  SLUG="proposal"
fi

out="$DEST_DIR/${DATE}-${SLUG}.md"
n=2
while [[ -e "$out" ]]; do
  out="$DEST_DIR/${DATE}-${SLUG}-${n}.md"
  n=$((n + 1))
done

# Fill only the date placeholder. Leave owner/status/body from the template.
sed "s/^date: YYYY-MM-DD$/date: ${DATE}/" "$TEMPLATE" > "$out"

rel="${out#"$ROOT"/}"
echo "Openlaw propose: $ROOT"
echo "Wrote $rel"
echo
echo "Next steps:"
cat <<'EOF'
  1. Fill Context, Decision, and Consequences in the new file.
  2. Open a pull request. Mark it as a proposal vs law change.
  3. Do not edit law/ or AGENTS.md in this PR.
  4. Only CODEOWNERS review and merge to law/ or AGENTS.md.
  5. Never auto-merge law. A proposed ADR is not binding.

This script is offline. It does not call the network and it does not
write secrets. It does not patch law/.
EOF
echo
echo "propose: done"
exit 0
