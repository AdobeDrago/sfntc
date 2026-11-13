# Rebuild all 13 sfntc.com sitemap pages as native EDS blocks

**Branch:** `sfntc-pages-parity` → `main`

**Preview** (every page in https://www.sfntc.com/page-sitemap.xml):
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/our-company
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/our-company/sfntc-vision
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/our-product
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/our-product/the-passion-behind-the-brand
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/transforming-tobacco
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/want-to-quit-smoking
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/underage-tobacco-prevention
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/our-commitment
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/our-commitment/cigarette-waste
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/our-commitment/carolina-farm-stewardship-association
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/our-commitment/what-you-can-do-to-help
- https://sfntc-pages-parity--sfntc--adobedrago.aem.page/sfntc-foundation

## What this changes
Every value was measured from the source's computed styles at 1440 and 1280. Nothing links to, or copies, the source site's CSS or JS.

- **Template:** `header` (parchment bar, logo card, 4 dropdowns, mobile toggle), `footer`, new `page-header` (title band + breadcrumb).
- **Existing blocks used / extended:** `hero` (home), `columns` (variant `contact`).
- **New blocks:** `cta` (image, banner, dual), `carousel`, `table`, `spacer` (DA drops empty paragraphs).
- **Shared code:** `scripts/scripts.js` (image aspect ratio from authored width/height, list-item paragraph unwrap, empty trailing section removal).
- **Section styles:** `band`, `highlight`, `quote`, `title-center`, `flush-image`, `space-after`, `space-after-list`, `end-gap`.
- **Fonts and images:** Oswald (OFL) and Open Sans 800 self-hosted; logo and parchment textures under `/images`; content images uploaded to DA.
- **Harness:** `import-work/` (ledger, gate configs, content tools; excluded from serving via `.hlxignore`).

## Content (DA)
All 13 pages copied verbatim from the source, plus fragments `/nav` and `/footer`. The "Enter SFNTC.com" welcome page that the source serves to visitors without its cookie is **not** migrated.

## Verification
Source measured in headless Chromium reusing a session the user passed in a headed window (reference bundles captured 2026-11-13). Sections gated at 1440 and 1280.

| Page | Local gate | Branch preview |
|---|---|---|
| home | 12/12 | all sections at position; hero 98.54% (re-encoded photo), photos unpaired |
| 11 inner pages | all sections pass | photo pairing only (`media_<hash>`), ~100% pixel |
| sfntc-foundation | 26/28 sections (2 residual style mismatches) | at position; photo pairing, footer 98.4% |

- Page offsets (`offsets.js`): 13/13 pages, every section at the source's page position (local and preview).
- Timelines: not run (carousel autoplay timing not measured; slide text and dots are `invisible` in `site.json`).
- `npm run lint` clean.
- Details and per-page residuals: `import-work/ledger.md`.

## Not covered
- Mobile / tablet widths (not scored), nav dropdown hover/open states (built, not gated), carousel autoplay, personalization.
- `sfntc-foundation`: `History` heading x-offset 4.4px (empty heading in the source) and top margin of the first photo (source class `alignnone`) differ by design limits of DA content.
- Home hero links to `/our-company/sfntc-vision/`; the source links to `/sfntc-vision/` (redirect not verified).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
