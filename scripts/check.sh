#!/usr/bin/env bash
# ------------------------------------------------------------------
# check.sh — run the project checks.
# Used by the pre-commit hook and GitHub CI.
# One command, everywhere the same → no "works on my machine".
#
# This project is a static site + offline image tools. There is no
# lint/type toolchain; tests use stdlib unittest only (no install).
# See docs/decisions/0001-baseline.md and 0002-site-generator.md.
# Everything below needs ZERO install.
# ------------------------------------------------------------------
set -uo pipefail
cd "$(dirname "$0")/.."          # run from the project root

fail=0
step() { echo; echo "▶ $1"; }
run()  { if ! "$@"; then echo "  ✗ FAIL: $*"; fail=1; fi; }

# ---------- JS syntax (node --check, no imports executed)
if compgen -G "site/assets/js/*.js" >/dev/null; then
  step "JS · syntax (node --check)"
  for f in site/assets/js/*.js; do run node --check "$f"; done
fi

# ---------- Python tools syntax (py_compile does NOT import the deps)
if compgen -G "tools/*.py" >/dev/null; then
  step "Python · syntax (py_compile)"
  run python3 -m py_compile tools/*.py
fi

# ---------- Generated site must match its sources (no hand-edits)
if [ -f tools/build_site.py ]; then
  step "Site · generated output is up to date"
  run python3 tools/build_site.py --check
  step "Site · tests (stdlib unittest)"
  run python3 tools/test_site.py
fi

# ---------- Shell syntax
step "Shell · syntax (bash -n)"
for f in tools/*.sh scripts/*.sh .githooks/*; do
  [ -f "$f" ] && run bash -n "$f"
done

echo
if [ "$fail" -ne 0 ]; then
  echo "❌ CHECK FAILED — fix the errors above before committing."
  exit 1
fi
echo "✅ ALL CHECKS PASS"
