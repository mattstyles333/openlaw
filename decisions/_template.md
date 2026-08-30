---
date: YYYY-MM-DD
owner: name-or-handle
status: proposed
supersedes:
---

# Title of the decision

Copied by `scripts/propose.sh`. Replace the title and fill the sections.
This file is a proposal. It is not law.

## Context

Why this is in front of us. What constraint, brand, SoR, or priority is
underspecified or wrong. Link any related ADRs.

## Decision

What we will do. Be specific enough that an owner can patch `law/` from
this section alone.

## Consequences

What becomes easier, what becomes harder, what we are explicitly not
doing. Name the files that must change (`law/constraints.md`,
`law/brand.md`, …) when this ADR is marked `decided`. Only CODEOWNERS
merge to `law/` or `AGENTS.md`. Never auto-merge law.
