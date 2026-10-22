# Architecture

## What this project actually is
A static portfolio site plus an offline image pipeline. There is no server and
no runtime dependency. Since 0002, the site's HTML is *generated* from templates
by a standard-library script; everything else is plain files.

```
docs/            editorial + strategy + art direction (French, human-facing)
site-src/        SOURCE for the website (edit here)
  layout.html    shared skeleton: <head>, script tag
  partials/      optional reusable fragments
  pages.json     per-page metadata (title, description, og, asset versions)
  pages/         per-page <main> content (*.body.html)
site/            GENERATED website (never edit by hand)
  assets/css     style.css — all art direction, variables at the top
  assets/js      site.js  — two IIFEs: cursor tracking + click ripple
  assets/img     images; produced by tools/*.py and tools/duotone.sh
  assets/video   generated videos (git-ignored except README.txt)
tools/           offline pipeline + site generator
  build_site.py  site-src/ -> site/  (stdlib only)
  test_site.py   stdlib unittest tests for the generated site
  make_lineart.py, make_backing.py, duotone.sh  image pipeline
scripts/         agent harness: check.sh, setup.sh
```

### Data flow
`site-src/` + `tools/build_site.py` → `site/` → served statically. Separately,
`tools/make_lineart.py`, `tools/make_backing.py` and `tools/duotone.sh` read raw
inputs and write into `site/assets/{img,video}`. The site only *reads* those
static files; nothing in `site/` imports anything at runtime.

### Shared front-end
`site/assets/css/style.css` and `site/assets/js/site.js` are unchanged plain
assets. `site.js` holds two IIFEs, cursor tracking and the click ripple. The
shared `<head>` and script tags are produced once from `site-src/layout.html`,
so the five pages can no longer drift from each other.
The visual system follows the "temporary" handoff: fluid `clamp()` sizes, a hero
that fits exactly one screen, and the same paper / crosses / serif / one-blue
direction.

## Why there is no automated architecture contract
- `import-linter` needs a Python package with intra-package imports. `tools/`
  is a set of standalone scripts → no contract to express.
- `dependency-cruiser` needs JS modules and a `package.json`. `site.js` is a
  single file with zero imports → nothing to enforce.
Both were intentionally NOT installed. See `docs/decisions/0001-baseline.md`.

## Current violations / known debt (observed, not aspirational)
- No lint/type checking and no HTML validation: `check.sh` covers syntax, the
  generated-site freshness and a small unittest suite only.
- `tools/` outputs are not reproducible in CI (opencv/scipy/ffmpeg are not
  installed there); only `build_site.py` and `test_site.py` are stdlib-only.
- `site/assets/img/og.png` is referenced but not committed yet.
- `cv.pdf` is referenced but not committed yet.
- `site-src/pages/*.body.html` still contain long single-line paragraphs; the
  generator preserves them verbatim rather than reformatting (no HTML formatter).

## Cross-cutting rules
- Never edit `site/*.html` by hand: edit `site-src/` then run
  `python3 tools/build_site.py`. `check.sh` enforces the output matches.
- No secrets in the repo; `.env*` is git-ignored and blocked by the pre-commit hook.
- Keep `site/` dependency-free: it must stay a folder you can drop on any host.
