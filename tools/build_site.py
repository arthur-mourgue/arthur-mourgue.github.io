#!/usr/bin/env python3
"""build_site.py: generate the static site/ pages from site-src/.

The site is plain HTML with no runtime dependency. To stop copy-pasting the
shared <head> and script tags across the five pages, the sources live in
site-src/ and this standard-library-only script assembles them into site/.

Workflow:
    edit site-src/                 (pages.json + pages/*.body.html + partials/)
    python3 tools/build_site.py    (regenerate site/)
    ./scripts/check.sh             (verifies the generated output is up to date)

Usage:
    python3 tools/build_site.py            # write site/
    python3 tools/build_site.py --check    # verify only, write nothing (CI)
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "site-src"
OUT_DIR = PROJECT_ROOT / "site"

INCLUDE_RE = re.compile(r"\{\{\s*include:([A-Za-z0-9_-]+)\s*\}\}")
TOKEN_RE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def resolve_includes(text: str, partials: dict[str, str], seen: tuple[str, ...] = ()) -> str:
    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        if name in seen:
            raise ValueError(f"recursive include: {' -> '.join(seen + (name,))}")
        if name not in partials:
            raise ValueError(f"unknown partial: {name}")
        return resolve_includes(partials[name], partials, seen + (name,))

    return INCLUDE_RE.sub(repl, text)


def render_page(
    page: dict,
    config: dict,
    layout: str,
    partials: dict[str, str],
    bodies: dict[str, str],
) -> str:
    output = page["output"]
    root = "../" * output.count("/")

    meta_description = ""
    if page.get("description"):
        meta_description = f'  <meta name="description" content="{esc(page["description"])}">\n'

    og_lines = []
    if page.get("og_comment"):
        og_lines.append(f'  <!-- {page["og_comment"]} -->')
    if page.get("og_title"):
        og_lines.append(f'  <meta property="og:title" content="{esc(page["og_title"])}">')
    if page.get("og_description"):
        og_lines.append(f'  <meta property="og:description" content="{esc(page["og_description"])}">')
    if page.get("og_image"):
        og_lines.append(f'  <meta property="og:image" content="{root}{page["og_image"]}">')
    og_tags = "".join(line + "\n" for line in og_lines)

    tokens = {
        "title": esc(page["title"]),
        "meta_description": meta_description,
        "og_tags": og_tags,
        "root": root,
        "css_version": str(config["css_version"]),
        "js_version": str(config["js_version"]),
        "body": bodies[page["body"]],
    }

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in tokens:
            raise ValueError(f"{output}: unknown token '{key}'")
        return tokens[key]

    return TOKEN_RE.sub(repl, resolve_includes(layout, partials))


def load() -> tuple[dict, str, dict[str, str], dict[str, str]]:
    config = json.loads((SRC_DIR / "pages.json").read_text(encoding="utf-8"))
    layout = (SRC_DIR / "layout.html").read_text(encoding="utf-8")
    partials = {p.stem: p.read_text(encoding="utf-8") for p in sorted((SRC_DIR / "partials").glob("*.html"))}
    bodies = {}
    for page in config["pages"]:
        bodies[page["body"]] = (SRC_DIR / "pages" / page["body"]).read_text(encoding="utf-8")
    return config, layout, partials, bodies


def render_all() -> dict[str, str]:
    """Render every page; returns {project-relative path: html}."""
    config, layout, partials, bodies = load()
    return {
        str((OUT_DIR / page["output"]).relative_to(PROJECT_ROOT)): render_page(
            page, config, layout, partials, bodies
        )
        for page in config["pages"]
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify site/ is up to date; write nothing")
    args = ap.parse_args()

    try:
        generated = render_all()
    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        stale = [
            path
            for path, text in generated.items()
            if not (PROJECT_ROOT / path).exists()
            or (PROJECT_ROOT / path).read_text(encoding="utf-8") != text
        ]
        if stale:
            print("site/ is out of date — run: python3 tools/build_site.py", file=sys.stderr)
            for path in stale:
                print(f"  stale: {path}", file=sys.stderr)
            return 1
        print(f"site/ is up to date ({len(generated)} pages)")
        return 0

    for path, text in generated.items():
        (PROJECT_ROOT / path).write_text(text, encoding="utf-8")
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
