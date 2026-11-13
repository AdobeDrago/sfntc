# Parity rebuild ledger: sfntc.com (13 pages)

Baseline at start: **not measured** (`get_usage` was first called after the build). At local-gate
completion: context 404,642 tokens (this session); account extra-usage meter $356.82 of $600 (shared
with the four parallel Reynolds sessions, so no per-row spend is claimed).
Gate: ≥99% pixel and 0 computed-style mismatches per section at 1440 and 1280 (default bar, not lowered),
plus section page offsets.

Per-row context/spend deltas were not recorded (no baseline). Mismatch and pixel figures are from
`gate.js` runs: "before" is the first run of that piece (rounded, some pieces were gated together), "after"
is the final run (`tools/run_all.sh`).

| Phase / iteration | Block / variant | Change | Mismatches before→after | Pixel before→after (1440 / 1280) | Context Δ | Spend Δ |
|---|---|---|---|---|---|---|
| Intake | — | Decided upstream: widths 1440+1280, images uploaded to DA, video poster only, open/dropdown states not gated, dynamic data = static placeholder marked `invisible`. Sitemap: 13 URLs. `preflight.js` said 13/13 `ok` but every page returned the same 1115-char text: the server serves an "Enter SFNTC.com" entry page to clients without its cookie. The user passed it in a headed window (profile `work/.browser-profile`); the gate itself is **not** rebuilt (user decision) | n/a | n/a | n/a | n/a |
| Capture | — | 13 bundles × 2 widths. First captures in headed mode; later ones in headless Chromium reusing the same user-passed session profile (`tools/headless-preload.js`) because headed rasterisation drifted from the headless rebuild (see residuals). `site.json` `freezeCss` hides scrollbars | n/a | n/a | n/a | n/a |
| Map | — | Two templates: home (4 sections) and inner (page-header, breadcrumb, entry-content). Reuse: `header`, `footer`, `hero`, `columns` (variant `contact`); new: `page-header`, `cta` (image / banner / dual), `carousel`, `table` | n/a | n/a | n/a | n/a |
| Template it.1–6 | header | logo + paper card (image used at 0.5×), parchment `auto 100%`, 4 dropdowns (CSS hover/focus, click on touch), nav 600/700px wide | 32→0 | 78.5 / 78.7 → 100 / 99.4 | | |
| Template it.1–3 | footer | span + links row, 60px, weight 500 face | 11→0 | 95.4 / 95.5 → 100 / 99.7 | | |
| Template it.1–3 | page-header | gray band, h1 + 3px orange underline, crumbs rebuilt as `p > span > span` | 2→0 | 99.1 → 99.8 | | |
| Template | fonts | Oswald (OFL) variable latin file declared as 300/500/600/700 faces (the source has no 400 face, so 400 resolves to 500); Open Sans 800 for buttons | n/a | n/a | | |
| Section | default content (inner pages) | 721px column, h2/h3, lists (ul 7px / ol 50px), links black/underlined, `band` highlight + quote, `title-center`, `space-after`, images (`<em>` = no top margin) | 22→0 | 88.9 → 100 | | |
| Section | hero (home) | photo as CSS background + 583px translucent card | 6→0 | 56 → 99.7 | | |
| Section | cta image / banner / dual (home) | flex layouts, photo as CSS background | 13→0 | 83 → 99.1 | | |
| Section | carousel (foundation) | statistic slides in one grid cell; text and dots `invisible` (the source rotates) | → 0 | 50 → 100 | | |
| Section | table (foundation) | real `<table>` from block rows | 133→0 | 74 → 100 | | |
| Section | columns `contact` (foundation) | flex 488/500 shrink to 721 | 6→0 | 95 → 99.9 | | |
| Page level | offsets | 13/13 pages, every section at the source's page Y (spacer gaps modelled as section margins) | n/a | n/a | | |
| Lint | — | `npm run lint` clean (import-work/ in `.eslintignore`) | n/a | n/a | | |

## Residuals (local gate, factual)
- **sfntc-foundation, `History` heading** (1 style mismatch, both widths): source x = 4.4px because an empty `<h2></h2>` sits before it on the same line; DA drops empty headings, so the rebuild starts at x = 0. Pixel 99.4%.
- **Source capture variance:** header/footer measured in headed Chromium differed from the headless rebuild by a sub-pixel text offset (97–99% pixel, text height 18 vs 17px). Capturing in headless Chromium with the same session profile gives 100%. All bundles in `work/bundles/` are the headless ones.
- **Carousel (foundation):** source autoplays; rotation timing was not measured, so the rebuild shows slide 1 with clickable dots and no autoplay. Slide text and dots are `invisible` in `site.json`, so they are not pixel-compared.
- **Hover / open states** (nav dropdowns) are built but not gated (intake decision).
- **Images:** local gate used the exact renditions the source browser painted (named in the style records). On the branch preview EDS renames and re-encodes images (`media_<hash>`), so image pairing and photo pixels are expected to differ.
- **Entry gate:** the "Enter SFNTC.com" welcome page is not migrated (user decision).
- **Home hero link:** the source links to `/sfntc-vision/`; the rebuild links to `/our-company/sfntc-vision/` (the sitemap URL of the vision page). Redirect behaviour of `/sfntc-vision/` was not verified.
- Footer text "© 2026 SFTNC." is copied verbatim (including the source's spelling).
