#!/usr/bin/env python3
"""tests for the generated site. Standard library only (unittest).

Run with:  python3 tools/test_site.py
Also run by ./scripts/check.sh.
"""
from __future__ import annotations

import html
import re
import unittest
from pathlib import Path

import build_site

# Local references that are intentional content TODO placeholders.
KNOWN_MISSING = {"cv.pdf"}

COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
ATTR_RE = re.compile(r'(?:href|src)="([^"]+)"')
P_RE = re.compile(r"<p\b[^>]*>(.*?)</p>", re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
REQUIRED_META = ('charset="utf-8"', 'name="viewport"', 'name="color-scheme"', 'rel="stylesheet"')


class GeneratedSiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = build_site.render_all()

    def test_generated_output_is_up_to_date(self) -> None:
        for path, expected in self.pages.items():
            with self.subTest(page=path):
                disk = build_site.PROJECT_ROOT / path
                self.assertTrue(disk.exists(), f"{path} is missing — run python3 tools/build_site.py")
                self.assertEqual(disk.read_text(encoding="utf-8"), expected,
                                 f"{path} is stale — run python3 tools/build_site.py")

    def test_every_page_has_required_meta(self) -> None:
        for path, text in self.pages.items():
            with self.subTest(page=path):
                self.assertRegex(text, r"<title>.+</title>")
                for needle in REQUIRED_META:
                    self.assertIn(needle, text, f"{path} is missing {needle}")

    def test_local_references_exist(self) -> None:
        for path, text in self.pages.items():
            base = (build_site.PROJECT_ROOT / path).parent
            body = COMMENT_RE.sub("", text)
            for url in ATTR_RE.findall(body):
                if url.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#")):
                    continue
                if "{{" in url:
                    continue  # unfilled content placeholder, e.g. {{LAMAIN_GITHUB_URL}}
                clean = url.split("?")[0].split("#")[0]
                if not clean or clean in KNOWN_MISSING:
                    continue
                with self.subTest(page=path, ref=url):
                    self.assertTrue((base / clean).exists(), f"{path}: broken reference {url}")

    def test_no_file_scheme(self) -> None:
        for path, text in self.pages.items():
            with self.subTest(page=path):
                self.assertNotIn("file://", text)

    def test_light_theme_only(self) -> None:
        for path, text in self.pages.items():
            with self.subTest(page=path):
                self.assertIn('<meta name="color-scheme" content="light">', text)
                self.assertNotIn("theme-toggle", text)
                self.assertNotIn("data-theme", text)

    def test_project_github_links(self) -> None:
        home = self.pages["site/index.html"]
        self.assertIn("https://github.com/Arthur-Mourgue/LaMain", home)
        self.assertIn("https://github.com/Arthur-Mourgue/LePotager", home)
        self.assertIn("https://github.com/Arthur-Mourgue/LaMain", self.pages["site/projects/lamain.html"])
        self.assertIn("https://github.com/Arthur-Mourgue/LePotager", self.pages["site/projects/lepotager.html"])

    def test_no_em_dash(self) -> None:
        for path, text in self.pages.items():
            with self.subTest(page=path):
                self.assertNotIn("—", text)

    def test_no_colon_in_paragraphs(self) -> None:
        for path, text in self.pages.items():
            body = COMMENT_RE.sub("", text)
            for paragraph in P_RE.findall(body):
                plain = html.unescape(TAG_RE.sub("", paragraph))
                with self.subTest(page=path, text=plain[:60]):
                    self.assertNotIn(":", plain)


if __name__ == "__main__":
    unittest.main(verbosity=2)
