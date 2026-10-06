---
name: pre-commit-check
description: 'Run the project quality gates before committing — lint, format, type check, tests — and report pass/fail with what to fix. Trigger for "check before I commit" or "run the gates".'
---
# Pre-Commit Check

Run the project's quality gates before a commit and report exactly what passes and
what blocks — so a bad commit never goes out.

## Steps
1. **Detect the toolchain** from the repo (manifest files): e.g. `package.json`
   (eslint/prettier/tsc/jest), `pyproject.toml` (ruff/mypy/pytest), `go.mod`
   (gofmt/go vet/go test), `Cargo.toml` (clippy/cargo test).
2. **Run the gates** in this order, capturing output:
   - format/lint
   - type check
   - build (if cheap)
   - tests
3. **Report** a compact scorecard: each gate ✅/❌, and for each ❌ the first
   actionable error (file:line) plus the command to re-run just that gate.

## Rules
- Do not modify files to make gates pass — report; the engineer fixes.
- If the repo has no gate tooling, say so and list the obvious checks you *did*
  run (e.g. `git diff --check`, trailing whitespace, `npm ls` for broken deps).
- Never commit on a red gate; end the run with a clear **ready / not-ready** verdict.
