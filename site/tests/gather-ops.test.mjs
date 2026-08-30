import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { after, test } from 'node:test';

import {
  gatherOps,
  HARNESS_PLACEHOLDER,
} from '../scripts/gather-ops.mjs';

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const roots = [];

function makeTree(layout) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ol-ops-'));
  roots.push(root);
  for (const [rel, content] of Object.entries(layout)) {
    const full = path.join(root, rel);
    fs.mkdirSync(path.dirname(full), { recursive: true });
    fs.writeFileSync(full, content, 'utf8');
  }
  return root;
}

after(() => {
  for (const root of roots) {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

const ADR = (status, title) => `---
date: 2026-01-01
owner: fixture
status: ${status}
supersedes:
---

# ${title}
`;

const WF = (name) => `name: ${name}
on:
  push:
  pull_request:
`;

test('ops page imports the shipped gatherer', () => {
  const page = fs.readFileSync(
    path.join(SITE, 'src', 'pages', 'ops', 'index.astro'),
    'utf8',
  );
  assert.match(page, /gatherOps/);
  assert.match(page, /scripts\/gather-ops\.mjs/);
});

test('no law/permissions.md → harness summary is the placeholder', () => {
  const root = makeTree({
    'AGENTS.md': 'always-on law is git markdown, never a vector store\n',
    'law/constraints.md': 'always-on\n',
    'decisions/2026-01-01-alpha.md': ADR('proposed', 'Alpha'),
    'decisions/2026-01-02-beta.md': ADR('proposed', 'Beta'),
    'decisions/2026-01-03-gamma.md': ADR('decided', 'Gamma'),
    'decisions/TEMPLATE.md': ADR('proposed', 'Template must not count'),
    'decisions/README.md': '# Decisions\n',
    '.github/workflows/law-check.yml': WF('law-check'),
    '.github/workflows/secret-scan.yml': WF('secret-scan'),
  });
  const ops = gatherOps(root);
  assert.equal(ops.harness.source, 'placeholder');
  assert.equal(ops.harness.summary, HARNESS_PLACEHOLDER);
  assert.equal(ops.liveDb, false);
  assert.equal(ops.ciHealth.summary.length > 0, true);
  assert.equal(ops.ciHealth.healthy, false);
  assert.ok(ops.ciHealth.missing.includes('agent-security'));
  assert.equal(
    ops.ciHealth.workflows.map((w) => w.name).sort().join(','),
    'law-check,secret-scan',
  );
});

test('fixture permissions.md present → summary is taken from that file, not the placeholder', () => {
  const needle = 'FIXTURE_PERM_NEEDLE_READ_PROPOSE_MERGE';
  const root = makeTree({
    'AGENTS.md': 'law\n',
    'law/permissions.md': `# Harness × capability

Parent/merge = CODEOWNERS / human.

| Harness | read | propose | merge |
| --- | --- | --- | --- |
| Herdr / Grok Build | yes | yes | no |
| ${needle} | yes | yes | no |
`,
    'decisions/2026-04-01-one.md': ADR('proposed', 'One'),
    'decisions/2026-04-02-two.md': ADR('proposed', 'Two'),
    'decisions/2026-04-03-three.md': ADR('proposed', 'Three'),
    'decisions/2026-04-04-four.md': ADR('decided', 'Four'),
    '.github/workflows/law-check.yml': WF('law-check'),
    '.github/workflows/secret-scan.yml': WF('secret-scan'),
    '.github/workflows/agent-security.yml': WF('agent-security'),
    '.github/workflows/mcp-test.yml': WF('mcp-test'),
  });
  const ops = gatherOps(root);
  assert.equal(ops.harness.source, 'permissions');
  assert.equal(ops.harness.summary.includes(needle), true);
  assert.equal(ops.harness.summary.includes(HARNESS_PLACEHOLDER), false);
  assert.equal(ops.harness.summary === HARNESS_PLACEHOLDER, false);
  assert.equal(ops.ciHealth.healthy, true);
});

test('fixture decisions/ with a known number of status: proposed ADRs', () => {
  const root = makeTree({
    'AGENTS.md': 'law\n',
    'law/constraints.md': 'always-on\n',
    'decisions/2026-04-01-one.md': ADR('proposed', 'One'),
    'decisions/2026-04-02-two.md': ADR('proposed', 'Two'),
    'decisions/2026-04-03-three.md': ADR('proposed', 'Three'),
    'decisions/2026-04-04-four.md': ADR('decided', 'Four'),
    'decisions/proposed/2026-04-05-five.md': ADR('proposed', 'Five'),
    'decisions/TEMPLATE.md': ADR('proposed', 'Template must not count'),
    'docs/OPS.md': '# Ops\n',
    'docs/WHY.md': '# Why\n',
  });
  const ops = gatherOps(root);
  assert.equal(ops.openProposals, 4);
  assert.equal(ops.proposals.length, 4);
  assert.equal(
    ops.proposals.every((p) => p.status === 'proposed' && p.path.endsWith('.md')),
    true,
  );
  assert.equal(
    ops.proposals.some((p) => p.path.includes('TEMPLATE')),
    false,
  );
  const hrefs = ops.markdownLinks.map((l) => l.href);
  assert.equal(
    hrefs.some((h) => h.endsWith('.md')),
    true,
  );
  assert.equal(
    ops.markdownLinks.some((l) => l.path === 'docs/OPS.md'),
    true,
  );
});
