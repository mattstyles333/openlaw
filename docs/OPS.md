# Ops dashboard

The GitHub Pages site ships a **build-time** ops one-pager at `/ops/`.
It is static HTML. There is no live database, no runtime GitHub poll,
and no memory product behind it.

## What it shows

Generated from this checkout when `site` builds:

- **CI health** — GitHub Actions workflow files under `.github/workflows/`
  (names, `on:` events, whether the required gates exist in git). Live
  run status stays on GitHub Actions; this page does not call an API.
- **Harness matrix summary** — `law/permissions.md` when that file is
  present. If it is absent, the page renders a placeholder. This slice
  does not create or edit `law/permissions.md`.
- **Open proposals** — count of `decisions/` ADRs with
  `status: proposed` (plus `decisions/proposed/*.md` when that directory
  exists). `TEMPLATE.md`, `README.md`, and `_index.md` are skipped.
- **Links out to `.md` files** — `AGENTS.md`, `law/`, `docs/`,
  `decisions/`, `examples/`, and a few root docs, pointing at GitHub
  blob URLs.

## How to build

From the repo root:

```bash
cd site
npm ci
npm run build
```

Astro emits `dist/ops/index.html` (with `base: '/openlaw/'`, the public
path is `/openlaw/ops/`). The page imports `site/scripts/gather-ops.mjs`
in frontmatter and calls `gatherOps()` against the repo root. That is
the only data path.

Inspect the same snapshot without a browser:

```bash
node site/scripts/gather-ops.mjs
```

Optional: `cd site && npm test` runs gatherer tests on temporary
fixture trees (placeholder vs `permissions.md`, known proposed counts).
`npm run test:built` asserts the built HTML after `npm run build`.

## What it does not do

- No SQLite, no Postgres, no vector store.
- No plugin SDK.
- No auto-write of `law/`.
- No fetch of GitHub check runs at request time.
- Pages deploy from `main` (see `.github/workflows/pages.yml`). Building
  this branch locally is how you prove the one-pager before merge.
