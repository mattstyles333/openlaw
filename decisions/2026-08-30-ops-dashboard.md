---
date: 2026-08-30
owner: openlaw-maintainers
status: proposed
supersedes:
---

# Ship a build-time ops one-pager on the existing site

## Context

Operators need a single place that answers: are the CI gates in git,
what may each harness do, how many ADRs are still `proposed`, and where
are the markdown files. That view must stay consistent with the product:
git is the system of record, not a dashboard database.

A live API or SQLite snapshot would become a second brain. Agents would
read the projection instead of the working tree. This repo already has
an Astro/Starlight site on GitHub Pages; the missing piece is a static
ops page generated at build from files already in git.

## Decision

Add one Tailwind ops page under `site/` (`/ops/`). At `astro build` it
reads repo markdown, workflow YAML, and `site/package.json`. It does
not open a database and it does not fetch GitHub at request time.

- CI health comes from `.github/workflows/*.yml` present in the
  checkout.
- Harness summary comes from `law/permissions.md` when that file
  exists; otherwise a placeholder. This decision does not add that file.
- Open proposal count comes from `decisions/` files with
  `status: proposed`.
- Links go out to `.md` files on GitHub.

`docs/OPS.md` is the human how-to. `site/scripts/gather-ops.mjs` is the
gatherer. Tests for it live under `site/` so this slice does not edit
`mcp/`.

## Consequences

- The Pages workflow on `main` will publish `/openlaw/ops/` once this
  lands. Until then, `cd site && npm run build` is the proof.
- `law/` and `decisions/` stay read-only inputs for the site. The
  gatherer must not write them.
- If `law/permissions.md` is still absent (owned by a sibling slice),
  the page stays honest via the placeholder instead of inventing a
  matrix.
- When this ADR is marked `decided`, no `law/constraints.md` patch is
  required; this is site/docs surface, not agent-loaded policy.
