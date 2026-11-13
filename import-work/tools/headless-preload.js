// Run capture.js's headed mode (user-passed session profile) in headless Chromium so the
// source is rasterised like the rebuild. Usage: node -r ./tools/headless-preload.js capture.js ...
const path = require('path');
const pw = require(path.join(process.env.HOME, '.claude/skills/eds-parity-rebuild/node_modules/playwright'));
const orig = pw.chromium.launchPersistentContext.bind(pw.chromium);
pw.chromium.launchPersistentContext = (dir, opts = {}) => orig(dir, { ...opts, headless: true });
