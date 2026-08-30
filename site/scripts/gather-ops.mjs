#!/usr/bin/env node
/**
 * Build-time ops snapshot. Reads repo markdown / workflow YAML / JSON.
 * No live database. No runtime GitHub API. Call from Astro frontmatter
 * or `node scripts/gather-ops.mjs [repoRoot]`.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));

export const HARNESS_PLACEHOLDER =
  'Harness permissions matrix is not in this tree yet. Placeholder until law/permissions.md exists. Parent/merge remains CODEOWNERS / human. Harnesses may read law and propose ADRs; they must not merge law.';

export const REQUIRED_GATES = [
  'law-check',
  'secret-scan',
  'agent-security',
  'mcp-test',
];

const SKIP_DECISION_NAMES = new Set([
  'TEMPLATE.md',
  'README.md',
  '_index.md',
  '_template.md',
]);

const GITHUB_BLOB = 'https://github.com/mattstyles333/openlaw/blob/main';

export function defaultRepoRoot() {
  const candidates = [
    process.cwd(),
    path.resolve(process.cwd(), '..'),
    path.resolve(SCRIPT_DIR, '../..'),
  ];
  for (const candidate of candidates) {
    if (
      fs.existsSync(path.join(candidate, 'AGENTS.md')) &&
      fs.existsSync(path.join(candidate, 'law'))
    ) {
      return candidate;
    }
  }
  return path.resolve(SCRIPT_DIR, '../..');
}

function readText(file) {
  return fs.readFileSync(file, 'utf8');
}

function exists(file) {
  try {
    return fs.existsSync(file);
  } catch {
    return false;
  }
}

function relPosix(root, file) {
  return path.relative(root, file).split(path.sep).join('/');
}

function githubHref(relPath) {
  return `${GITHUB_BLOB}/${relPath}`;
}

function listDir(dir) {
  if (!exists(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true });
}

function walkMd(dir, acc = []) {
  if (!exists(dir)) return acc;
  for (const ent of listDir(dir)) {
    if (ent.name === 'node_modules' || ent.name === 'dist' || ent.name === '.git') {
      continue;
    }
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      walkMd(full, acc);
    } else if (ent.isFile() && ent.name.endsWith('.md')) {
      acc.push(full);
    }
  }
  return acc;
}

function extractOnEvents(text) {
  const inlineList = text.match(/^on:\s*\[([^\]]+)\]/m);
  if (inlineList) {
    return inlineList[1]
      .split(',')
      .map((s) => s.trim().replace(/^["']|["']$/g, ''))
      .filter(Boolean);
  }
  const inline = text.match(/^on:\s*([A-Za-z_][A-Za-z0-9_]*)\s*$/m);
  if (inline) return [inline[1]];
  const block = text.match(/^on:\s*\n((?:[ \t]+.*\n?)*)/m);
  if (!block) return [];
  const lines = block[1].split('\n').filter((line) => line.trim());
  if (!lines.length) return [];
  const indentMatch = lines[0].match(/^([ \t]+)/);
  const indent = indentMatch ? indentMatch[1] : '  ';
  const events = [];
  for (const line of lines) {
    if (!line.startsWith(indent)) continue;
    const rest = line.slice(indent.length);
    if (/^[ \t]/.test(rest)) continue;
    const match = rest.match(/^([A-Za-z_][A-Za-z0-9_]*):/);
    if (match) events.push(match[1]);
  }
  return events;
}

export function gatherCiHealth(root) {
  const dir = path.join(root, '.github', 'workflows');
  const workflows = [];
  if (exists(dir)) {
    for (const ent of listDir(dir)) {
      if (!ent.isFile() || !/\.ya?ml$/i.test(ent.name)) continue;
      const file = path.join(dir, ent.name);
      const text = readText(file);
      const nameMatch = text.match(/^name:\s*(.+)$/m);
      const name = nameMatch
        ? nameMatch[1].trim().replace(/^["']|["']$/g, '')
        : ent.name.replace(/\.ya?ml$/i, '');
      workflows.push({
        file: `.github/workflows/${ent.name}`,
        name,
        present: true,
        on: extractOnEvents(text),
      });
    }
    workflows.sort((a, b) => a.name.localeCompare(b.name));
  }
  const stems = new Set(
    workflows.map((w) => path.basename(w.file).replace(/\.ya?ml$/i, '')),
  );
  const names = new Set(workflows.map((w) => w.name));
  const missing = REQUIRED_GATES.filter((gate) => !stems.has(gate) && !names.has(gate));
  const healthy = missing.length === 0 && workflows.length > 0;
  let summary;
  if (workflows.length === 0) {
    summary =
      'No GitHub Actions workflow files found in this tree at build. CI health is unknown until workflows land in git.';
  } else if (healthy) {
    summary = `${workflows.length} workflow files in git at build. Required gates present: ${REQUIRED_GATES.join(', ')}. Live run status is GitHub Actions; this page does not poll an API.`;
  } else {
    summary = `${workflows.length} workflow files in git at build (${workflows.map((w) => w.name).join(', ')}). Missing required gates: ${missing.join(', ')}.`;
  }
  return { summary, workflows, healthy, missing };
}

function summarizePermissions(text) {
  const lines = text.split(/\r?\n/);
  const heading = (lines.find((line) => /^#\s+/.test(line)) || '')
    .replace(/^#\s+/, '')
    .trim();
  const tableLines = [];
  let inTable = false;
  for (const line of lines) {
    if (/^\s*\|/.test(line)) {
      inTable = true;
      tableLines.push(line.trim());
    } else if (inTable) {
      break;
    }
  }
  const stripped = text.replace(/^---[\s\S]*?---\s*/, '').trim();
  const body = tableLines.length ? tableLines.join('\n') : stripped.slice(0, 2000);
  return [heading, body].filter(Boolean).join('\n\n').slice(0, 4000);
}

export function gatherHarness(root) {
  const rel = 'law/permissions.md';
  const file = path.join(root, rel);
  if (!exists(file)) {
    return {
      source: 'placeholder',
      summary: HARNESS_PLACEHOLDER,
      path: rel,
    };
  }
  const text = readText(file);
  return {
    source: 'permissions',
    summary: summarizePermissions(text),
    path: rel,
    href: githubHref(rel),
  };
}

function isDecisionCandidate(relFromDecisions) {
  const base = path.basename(relFromDecisions);
  if (SKIP_DECISION_NAMES.has(base)) return false;
  if (!base.endsWith('.md')) return false;
  const posix = relFromDecisions.split(path.sep).join('/');
  if (/^20[^/]*\.md$/.test(base)) return true;
  if (posix.startsWith('proposed/') && base !== '.gitkeep') return true;
  return false;
}

export function gatherProposals(root) {
  const dir = path.join(root, 'decisions');
  const items = [];
  for (const file of walkMd(dir)) {
    const relFromDecisions = path.relative(dir, file);
    if (!isDecisionCandidate(relFromDecisions)) continue;
    const text = readText(file);
    const statusMatch = text.match(
      /^status:\s*(proposed|decided|superseded)\s*$/m,
    );
    if (!statusMatch || statusMatch[1] !== 'proposed') continue;
    const rel = relPosix(root, file);
    items.push({
      path: rel,
      status: 'proposed',
      href: githubHref(rel),
    });
  }
  items.sort((a, b) => a.path.localeCompare(b.path));
  return { count: items.length, items };
}

function collectMd(root, relDirOrFile, acc) {
  const full = path.join(root, relDirOrFile);
  if (!exists(full)) return;
  const stat = fs.statSync(full);
  if (stat.isFile() && full.endsWith('.md')) {
    acc.push(relPosix(root, full));
    return;
  }
  if (!stat.isDirectory()) return;
  for (const file of walkMd(full)) {
    acc.push(relPosix(root, file));
  }
}

export function gatherMarkdownLinks(root) {
  const acc = [];
  for (const item of [
    'AGENTS.md',
    'README.md',
    'SECURITY.md',
    'CONTRIBUTING.md',
    'CHANGELOG.md',
    'law',
    'docs',
    'decisions',
    'examples',
  ]) {
    collectMd(root, item, acc);
  }
  const unique = [...new Set(acc)].sort();
  return unique.map((relPath) => ({
    label: relPath,
    path: relPath,
    href: githubHref(relPath),
  }));
}

function readPkgVersion(root) {
  const pkgPath = path.join(root, 'site', 'package.json');
  if (!exists(pkgPath)) return null;
  try {
    const pkg = JSON.parse(readText(pkgPath));
    return typeof pkg.version === 'string' ? pkg.version : null;
  } catch {
    return null;
  }
}

/**
 * @param {string} [root]
 * @returns {{
 *   generatedAt: string,
 *   liveDb: false,
 *   siteVersion: string | null,
 *   ciHealth: ReturnType<typeof gatherCiHealth>,
 *   harness: ReturnType<typeof gatherHarness>,
 *   openProposals: number,
 *   proposals: { path: string, status: string, href: string }[],
 *   markdownLinks: { label: string, path: string, href: string }[],
 * }}
 */
export function gatherOps(root = defaultRepoRoot()) {
  const resolved = path.resolve(root);
  const ciHealth = gatherCiHealth(resolved);
  const harness = gatherHarness(resolved);
  const proposals = gatherProposals(resolved);
  const markdownLinks = gatherMarkdownLinks(resolved);
  return {
    generatedAt: new Date().toISOString(),
    liveDb: false,
    siteVersion: readPkgVersion(resolved),
    ciHealth,
    harness,
    openProposals: proposals.count,
    proposals: proposals.items,
    markdownLinks,
  };
}

const isMain =
  process.argv[1] &&
  path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (isMain) {
  const root = process.argv[2] ? path.resolve(process.argv[2]) : defaultRepoRoot();
  process.stdout.write(`${JSON.stringify(gatherOps(root), null, 2)}\n`);
}
