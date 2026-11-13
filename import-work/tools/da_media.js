#!/usr/bin/env node
// Upload the local media files that DA bodies reference (/media/...) to DA, and rewrite the
// bodies to point at the uploaded files, so the pipeline ingests them as EDS media.
// Usage: DA_TOKEN=... node tools/da_media.js [--yes]      (dry run without --yes)
// The token is read from the environment only; never pass it as an argument.
// sequential CLI tool, not site code:
/* eslint-disable no-console, no-restricted-syntax, no-continue, no-await-in-loop */
const fs = require('fs');
const path = require('path');

const base = path.resolve(__dirname, '..');
const cfg = JSON.parse(fs.readFileSync(path.join(base, 'pages.json'), 'utf8'));
const { org, site } = cfg.da;
const repo = path.resolve(base, cfg.repo);
const daDir = path.join(base, cfg.da.dir || 'da');
const yes = process.argv.includes('--yes');
const token = process.env.DA_TOKEN;
if (yes && !token) { console.error('DA_TOKEN is not set'); process.exit(1); }

const TYPES = {
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp',
};

(async () => {
  const bodies = fs.readdirSync(daDir).filter((f) => f.endsWith('.html'));
  const refs = new Set();
  bodies.forEach((f) => {
    const html = fs.readFileSync(path.join(daDir, f), 'utf8');
    for (const m of html.matchAll(/src="(\/media\/[^"]+)"/g)) refs.add(m[1]);
  });
  for (const ref of refs) {
    const file = path.join(repo, ref);
    if (!fs.existsSync(file)) { console.log(`missing local file for ${ref}`); process.exitCode = 1; continue; }
    const url = `https://admin.da.live/source/${org}/${site}${ref}`;
    if (!yes) { console.log(`dry run: PUT ${url} (${fs.statSync(file).size}b)`); continue; }
    const form = new FormData();
    form.append('data', new Blob([fs.readFileSync(file)], { type: TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' }), path.basename(file));
    const r = await fetch(url, { method: 'PUT', headers: { Authorization: `Bearer ${token}` }, body: form });
    console.log(`${ref}: ${r.status}`);
    if (!r.ok) process.exitCode = 1;
  }
  if (!yes || process.exitCode) return;
  bodies.forEach((f) => {
    const p = path.join(daDir, f);
    const html = fs.readFileSync(p, 'utf8');
    const out = html.replace(/src="(\/media\/[^"]+)"/g, (m, ref) => `src="https://content.da.live/${org}/${site}${ref}"`);
    if (out !== html) { fs.writeFileSync(p, out); console.log(`rewrote ${f}`); }
  });
})();
