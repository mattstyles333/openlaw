#!/usr/bin/env bash
# Openlaw local CI — the agent security layer for law files.
#
# ADOPTERS: replace the three grep needles in NEEDLE_* below with your
# organisation's non-negotiable hard rules. Use the SAME strings you
# inline in AGENTS.md. The defaults match the Northwind Coffee template
# and are not universal policy.
#
# Checks (fail closed, clear messages, exit non-zero on any failure):
#   1. Required files exist
#   2. AGENTS.md max 12000 bytes
#   3. AGENTS.md max 80 lines
#   4. Hard-rule needles in AGENTS.md and law/constraints.md
#   5. law/permissions.md capability needles (read, propose, merge, CODEOWNERS parent)
#   6. decisions/20*.md frontmatter (date, owner, status)
#   7. No secret patterns in law/ or AGENTS.md
#   8. CODEOWNERS covers law/ and AGENTS.md
#   9. If mcp/server.py exists: fail-closed auth, no execute_sql
#
# Usage: bash scripts/check-law.sh   # from repo root, or anywhere inside

set -euo pipefail

# --- needles (ADOPTERS: replace these) --------------------------------
NEEDLE_NO_INVENT="MUST never invent company policy"
NEEDLE_GIT_MARKDOWN="always-on law is git markdown, never a vector store"
NEEDLE_PROPOSE="MUST propose decisions; do not edit law/constraints.md without review"
# constraints.md is allowed a shorter form of the second needle:
NEEDLE_ALWAYS_ON="always-on"
NEEDLE_PROPOSE_SHORT="MUST propose decisions"
# ----------------------------------------------------------------------

fail_count=0
fail() { echo "FAIL: $*" >&2; fail_count=$((fail_count + 1)); }
ok()   { echo "ok: $*"; }

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
echo "Openlaw check-law: $ROOT"

# 1. Required files ----------------------------------------------------
REQUIRED=(
  LICENSE
  README.md
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  CODEOWNERS
  SECURITY.md
  CONTRIBUTING.md
  law/constraints.md
  law/brand.md
  law/sor.md
  law/priorities.md
  law/permissions.md
  decisions/README.md
  decisions/TEMPLATE.md
  decisions/_index.md
  docs/WHY.md
  docs/SECURITY-MODEL.md
  docs/HARNESS.md
  examples/grok-bot.md
  examples/grok-build.md
  examples/herdr.md
  examples/hermes.md
  examples/opencode.md
  examples/claude.md
  examples/gemini.md
  llms.txt
  scripts/reset-onboarding.sh
)
for f in "${REQUIRED[@]}"; do
  if [[ -f "$f" ]]; then
    ok "exists $f"
  else
    fail "missing required file: $f"
  fi
done

# 2–3. AGENTS.md size --------------------------------------------------
if [[ -f AGENTS.md ]]; then
  bytes=$(wc -c < AGENTS.md)
  lines=$(wc -l < AGENTS.md)
  bytes=${bytes// /}
  lines=${lines// /}
  if (( bytes > 12000 )); then
    fail "AGENTS.md is ${bytes} bytes (max 12000). Keep it short; put detail in law/."
  else
    ok "AGENTS.md ${bytes} bytes (<= 12000)"
  fi
  if (( lines > 80 )); then
    fail "AGENTS.md is ${lines} lines (max 80). Always-on law that does not fit the window is not always-on."
  else
    ok "AGENTS.md ${lines} lines (<= 80)"
  fi
fi

# 4. Hard-rule needles -------------------------------------------------
contains() {
  local file="$1" needle="$2"
  grep -F -q -- "$needle" "$file"
}

if [[ -f AGENTS.md ]]; then
  if contains AGENTS.md "$NEEDLE_NO_INVENT"; then
    ok "AGENTS.md has needle: $NEEDLE_NO_INVENT"
  else
    fail "AGENTS.md missing needle: $NEEDLE_NO_INVENT"
  fi
  if contains AGENTS.md "$NEEDLE_GIT_MARKDOWN"; then
    ok "AGENTS.md has needle: $NEEDLE_GIT_MARKDOWN"
  else
    fail "AGENTS.md missing needle: $NEEDLE_GIT_MARKDOWN"
  fi
  if contains AGENTS.md "$NEEDLE_PROPOSE"; then
    ok "AGENTS.md has needle: $NEEDLE_PROPOSE"
  else
    fail "AGENTS.md missing needle: $NEEDLE_PROPOSE"
  fi
fi

if [[ -f law/constraints.md ]]; then
  if contains law/constraints.md "$NEEDLE_ALWAYS_ON"; then
    ok "law/constraints.md has needle: $NEEDLE_ALWAYS_ON"
  else
    fail "law/constraints.md missing needle: $NEEDLE_ALWAYS_ON"
  fi
  if contains law/constraints.md "$NEEDLE_NO_INVENT"; then
    ok "law/constraints.md has needle: $NEEDLE_NO_INVENT"
  else
    fail "law/constraints.md missing needle: $NEEDLE_NO_INVENT"
  fi
  if contains law/constraints.md "$NEEDLE_PROPOSE_SHORT"; then
    ok "law/constraints.md has needle: $NEEDLE_PROPOSE_SHORT"
  else
    fail "law/constraints.md missing needle: $NEEDLE_PROPOSE_SHORT"
  fi
fi

# 5. Permissions matrix needles (target law/permissions.md only) -------
#    Short substrings (read) must not be grepped against the whole tree.
PERM_NEEDLES=(
  read
  propose
  merge
  CODEOWNERS
  parent
)
if [[ -f law/permissions.md ]]; then
  for needle in "${PERM_NEEDLES[@]}"; do
    if contains law/permissions.md "$needle"; then
      ok "law/permissions.md has needle: $needle"
    else
      fail "law/permissions.md missing needle: $needle"
    fi
  done
fi

# 6. Decision frontmatter ----------------------------------------------
shopt -s nullglob
decision_files=(decisions/20*.md)
shopt -u nullglob
if ((${#decision_files[@]} == 0)); then
  echo "note: no decisions/20*.md files yet"
else
  for f in "${decision_files[@]}"; do
    if ! grep -q '^date:' "$f"; then
      fail "$f missing frontmatter field date:"
    fi
    if ! grep -q '^owner:' "$f"; then
      fail "$f missing frontmatter field owner:"
    fi
    if ! grep -Eq '^status:[[:space:]]*(proposed|decided|superseded)[[:space:]]*$' "$f"; then
      fail "$f missing frontmatter status: proposed|decided|superseded"
    else
      ok "$f frontmatter date/owner/status"
    fi
  done
fi

# 7. Secret patterns in law/ and AGENTS.md -----------------------------
# Docs (SECURITY.md, docs/) may name token types. law/ and AGENTS.md may not
# contain credential *values* or common token prefixes.
SECRET_PATTERN='API_KEY=|BEGIN RSA PRIVATE KEY|sk-live-|ghp_|gho_|password:'
secret_hits=$(grep -R -n -E -- "$SECRET_PATTERN" law AGENTS.md decisions examples 2>/dev/null || true)
if [[ -n "$secret_hits" ]]; then
  echo "$secret_hits" >&2
  fail "secret-like pattern in law/, AGENTS.md, decisions/, or examples/ (API_KEY=, BEGIN RSA PRIVATE KEY, sk-live-, ghp_, gho_, password:)"
else
  ok "no secret patterns in law/, AGENTS.md, decisions/, or examples/"
fi
if [[ -f docker-compose.yml ]] && grep -Eq 'CANON_MCP_TOKEN:-\S' docker-compose.yml; then
  fail "docker-compose.yml must not default CANON_MCP_TOKEN (no fallback secret)"
elif [[ -f docker-compose.yml ]]; then
  ok "docker-compose.yml has no CANON_MCP_TOKEN default"
fi
if [[ -f docker-compose.yml ]]; then
  if grep -q '5432' docker-compose.yml; then
    fail "docker-compose.yml must not publish 5432"
  fi
  if grep -Eq '^[[:space:]]+postgres:' docker-compose.yml; then
    fail "docker-compose.yml must not ship a postgres service"
  fi
  if ! grep -q 'ghcr.io/mattstyles333/canon-mcp:0.1.0' docker-compose.yml; then
    fail "docker-compose.yml must pin ghcr.io/mattstyles333/canon-mcp:0.1.0"
  else
    ok "docker-compose.yml is GHCR pin :0.1.0 with no postgres/5432"
  fi
fi

# 8. CODEOWNERS --------------------------------------------------------
if [[ -f CODEOWNERS ]]; then
  if grep -q 'law/' CODEOWNERS; then
    ok "CODEOWNERS covers law/"
  else
    fail "CODEOWNERS does not mention law/"
  fi
  if grep -q 'AGENTS.md' CODEOWNERS; then
    ok "CODEOWNERS covers AGENTS.md"
  else
    fail "CODEOWNERS does not mention AGENTS.md"
  fi
fi

# 9. MCP fail-closed (only if mcp/server.py exists) --------------------
if [[ -f mcp/server.py ]]; then
  sql_hits=$(grep -R -n --include='*.py' --exclude-dir=.venv --exclude-dir=tests --exclude-dir=__pycache__ --exclude-dir=.pytest_cache -e 'execute_sql' mcp/ 2>/dev/null || true)
  if [[ -n "$sql_hits" ]]; then
    echo "$sql_hits" >&2
    fail "execute_sql is forbidden under mcp/ (shipped code, not tests)"
  else
    ok "mcp/ shipped python has no execute_sql"
  fi
  if grep -Eqi 'unauthenticated default|allow_anonymous|auth.*=.*none|AUTH_DISABLED' mcp/server.py; then
    fail "mcp/server.py looks like it defaults to unauthenticated"
  fi
  missing_auth=0
  grep -Eqi 'bearer' mcp/server.py || missing_auth=1
  grep -Eq '401' mcp/server.py || missing_auth=1
  grep -Eq 'CANON_COMMIT_TOKEN' mcp/server.py || missing_auth=1
  if ! grep -Eqi 'fail closed|fail-closed|refuse to listen|fails closed' mcp/server.py; then
    missing_auth=1
  fi
  if (( missing_auth == 1 )); then
    fail "mcp/server.py must fail closed (bearer, 401, CANON_COMMIT_TOKEN, fail closed language)"
  else
    ok "mcp/server.py fail-closed markers present"
  fi
else
  echo "note: mcp/server.py absent; skipping MCP auth gates (projection is optional)"
fi

# 10. Forbidden product-name tokens (needles live in this script; exclude it).
#    Phrase "always-on law" is allowed. Hyphenated token always-law is not.
leftover_hits=$(grep -RIn -E --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=.pytest_cache --exclude-dir='*.egg-info' --exclude-dir=node_modules --exclude-dir=dist --exclude=check-law.sh --exclude=.git \
  'AlwaysLaw|alwayslaw|always-law|[^N]LAW_MCP|\bCanon\b' . 2>/dev/null || true)
if [[ -n "$leftover_hits" ]]; then
  echo "$leftover_hits" >&2
  fail "forbidden product-name token in public tree"
else
  ok "no forbidden product-name tokens in public tree"
fi

echo
if (( fail_count > 0 )); then
  echo "check-law: $fail_count failure(s)" >&2
  exit 1
fi
echo "check-law: all gates passed"
exit 0
