# Decisions (ADRs)

Architecture Decision Records for Canon law. This is how policy
changes: **propose**, then **owners merge**.

Agents MUST propose decisions. They MUST NOT edit `law/constraints.md`
without review.

## Format

Copy [TEMPLATE.md](TEMPLATE.md). Frontmatter is required (CI greps it):

```yaml
date: YYYY-MM-DD
owner: name-or-handle
status: proposed   # proposed | decided | superseded
supersedes:        # filename or empty
```

Body sections: **Context** / **Decision** / **Consequences**.

Filenames: `YYYY-MM-DD-short-slug.md`. Keep slugs lowercase and
hyphenated.

## How to propose

1. Add `decisions/YYYY-MM-DD-slug.md` with `status: proposed`.
2. One-line it at the top of [_index.md](_index.md) (newest first).
3. Open a pull request. Do not edit `law/` in the same PR unless an
   owner has already marked the ADR `decided` and asked for the law
   patch.

## How to merge a decided ADR

Owners listed in `CODEOWNERS` review. On accept they:

1. Set `status: decided` (or `superseded` if this ADR replaces another).
2. Apply the corresponding change to `law/` (constraints, brand, SoR,
   or priorities).
3. Merge via the required-review path. `law/**` and `AGENTS.md` require
   owners.

A decided ADR is not law until `law/` says so. The ADR is the record of
*why*; `law/` is what agents load.

## Status

| status | meaning |
| --- | --- |
| `proposed` | specialist wrote it; not binding |
| `decided` | owners accepted; law/ should reflect it |
| `superseded` | a later ADR replaced it; leave the file in place |
