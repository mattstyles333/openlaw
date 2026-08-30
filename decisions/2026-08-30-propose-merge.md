---
date: 2026-08-30
owner: openlaw-maintainers
status: proposed
supersedes:
---

# Propose → review → merge; never auto-merge law

## Context

Openlaw is git law, not a memory product. Agents already have a hard
rule: propose decisions; do not edit `law/constraints.md` without
review. What was missing is a one-command draft path, a folder for
unmerged proposals, and a pull-request prompt that forces the author to
say whether the change is a **proposal vs law change**.

Without that loop, a helpful agent can treat a chat conclusion as
policy and patch `law/` in the same branch. That is keys to the castle.

## Decision

The learning loop is **propose → review → merge**:

- Any harness may propose an ADR or skill under `decisions/proposed/`
  (or under `decisions/` with `status: proposed`).
- Every harness proposes via a **GitHub PR**. The pull request is the
  discussion room. Silent file writes to `law/` are not a proposal.
- `scripts/propose.sh` copies `decisions/_template.md` and prints next
  steps. It is offline. It does not write `law/` or `AGENTS.md`.
- Pairing: `.github/workflows/pr-law-review.yml` runs `check-law.sh` on
  `pull_request` and comments suggested improvements (fail soft if it
  cannot comment). Optional harness webhook, where supported, watches
  that same PR. Neither half merges.
- Only CODEOWNERS merge to `law/` or `AGENTS.md`. Never auto-merge law.

See `docs/LEARNING.md`.

## Consequences

- Draft ADRs can land without touching binding files.
- A PR that mixes a proposal and a `law/` edit is the wrong kind of
  change until an owner has marked the ADR `decided`.
- Auto-merge, plugin SDKs, and a SQLite brain are out of scope. This
  ADR does not grant any harness merge rights on `law/` or `AGENTS.md`.
