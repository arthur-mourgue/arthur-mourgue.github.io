# 0001 — Baseline: no lint/type/test toolchain

Date: 2026-09-28
Status: accepted

## Context
The project had **no** automated quality tooling: no test framework, no
linter, no type checker, no formatter, and no CI. It is a static site
(HTML/CSS/vanilla JS) plus a small offline Python/ffmpeg image pipeline.

Adding a real toolchain (eslint, ruff, mypy, a test runner) would mean
installing dependencies and could flag a large amount of existing code.
The existing code was kept as-is rather than mass-fixed.

## Decision
`scripts/check.sh` only checks what requires no new dependency:
- JS parses (`node --check`),
- Python tools parse (`python3 -m py_compile`, which does not import the deps),
- shell scripts parse (`bash -n`).

**Baseline**: the existing code is accepted as-is. Any *new* code must pass
`./scripts/check.sh`. Introducing eslint/ruff/mypy/tests is a separate,
explicit decision to be made later.

## Consequences
- The check is weak by design: it cannot catch logic bugs, style or dead code.
- `check.sh` must not be weakened or silenced to make a change pass.
- If a real toolchain is added later, do it as its own feature, run it once to
  record the existing violations, and only then make it blocking.
