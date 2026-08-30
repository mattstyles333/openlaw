import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HTML = path.join(SITE, 'dist', 'ops', 'index.html');

function readBuiltCss(html) {
  const astroDir = path.join(SITE, 'dist', '_astro');
  let css = '';
  if (fs.existsSync(astroDir)) {
    for (const name of fs.readdirSync(astroDir)) {
      if (name.endsWith('.css')) {
        css += fs.readFileSync(path.join(astroDir, name), 'utf8');
      }
    }
  }
  const linked = [...html.matchAll(/href="([^"]+\.css)"/g)].map((m) => m[1]);
  for (const href of linked) {
    const rel = href.replace(/^\/openlaw\//, '').replace(/^\//, '');
    const candidates = [
      path.join(SITE, 'dist', rel),
      path.join(SITE, 'dist', path.basename(rel)),
    ];
    for (const candidate of candidates) {
      if (fs.existsSync(candidate)) {
        css += fs.readFileSync(candidate, 'utf8');
      }
    }
  }
  const inline = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)];
  for (const block of inline) css += block[1];
  return css;
}

test('built ops HTML has CI health, harness or placeholder, proposal count, md hrefs, Tailwind', () => {
  assert.equal(fs.existsSync(HTML), true, `missing ${HTML}; run npm run build`);
  const html = fs.readFileSync(HTML, 'utf8');

  const ci = html.match(
    /data-ops="ci-health-summary"[^>]*>([\s\S]*?)<\/p>/,
  );
  assert.ok(ci, 'CI health summary marker missing');
  assert.ok(ci[1].replace(/<[^>]+>/g, '').trim().length > 0, 'CI health empty');

  assert.match(html, /data-ops="harness-summary"/);
  assert.match(html, /data-ops="harness-source"/);
  assert.match(html, /Placeholder|law\/permissions\.md|Harness permissions matrix/);

  const count = html.match(
    /data-ops="open-proposals-count"[^>]*>([\s\S]*?)<\/p>/,
  );
  assert.ok(count, 'open proposals count missing');
  assert.match(count[1], /\d+/);

  assert.match(html, /href="[^"]+\.md"/);

  const pkg = JSON.parse(fs.readFileSync(path.join(SITE, 'package.json'), 'utf8'));
  assert.ok(pkg.dependencies?.tailwindcss, 'tailwindcss must be a site dependency');
  assert.ok(
    pkg.dependencies?.['@tailwindcss/vite'],
    '@tailwindcss/vite must be a site dependency',
  );

  assert.match(html, /min-h-screen/);
  assert.match(html, /\bgrid\b/);

  const css = readBuiltCss(html);
  const tw =
    css.includes('display:grid') ||
    css.includes('.grid{') ||
    css.includes('.min-h-screen') ||
    css.includes('min-height:100vh') ||
    /--tw/.test(css);
  assert.equal(tw, true, 'built CSS does not contain Tailwind utility output');
});
