# Arthur Mourgue — Portfolio

Personal portfolio of Arthur Mourgue, robotics engineer in AI and perception.
Live at [arthur-mourgue.github.io](https://arthur-mourgue.github.io).

## Stack

Plain HTML, CSS and JavaScript. No framework, no runtime dependency. The pages
are generated from `site-src/` by a standard-library Python script.

## Structure

- `site-src/` — page sources (`pages.json`, `layout.html`, `pages/*.body.html`)
- `site/` — generated site, served by GitHub Pages
- `tools/` — site generator, tests and offline image pipeline
- `docs/` — architecture notes and design decisions
- `scripts/check.sh` — syntax, generated-site freshness and tests

## Build

```bash
python3 tools/build_site.py
```

## Check

```bash
./scripts/check.sh
```

## Preview

```bash
python3 -m http.server 8000 --directory site
```

Then open <http://localhost:8000>.

## Deploy

Pushes to `master` deploy `site/` to GitHub Pages through GitHub Actions.
