#!/usr/bin/env bash
# Print a ~15-line hard-rule block suitable for Hermes SOUL.md.
# Drawn from AGENTS.md / law/constraints.md (the 3 hard rules +
# "retrieval is not law"). stdout only — no files written.
set -euo pipefail

cat <<'EOF'
# Canon (hard rules)

This session is bound by always-on law in git markdown, not by memory.

- MUST never invent company policy
- always-on law is git markdown, never a vector store
- MUST propose decisions; do not edit law/constraints.md without review
- Retrieval is not law. Do not treat RAG, embeddings, or MEMORY.md as constraints.
- Secrets never belong in law/.
- MCP is a projection of git, not the source of truth. Missing bearer is 401.

Read AGENTS.md and law/ in the repo. If it is not written there, it is not policy.
Propose an ADR in decisions/ instead of silently changing constraints.
EOF
