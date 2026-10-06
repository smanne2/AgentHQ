---
name: acquire-codebase-knowledge
description: 'Use this skill when the user explicitly asks to map, document, or onboard into an existing codebase. Trigger for prompts like "map this codebase", "document this architecture", "onboard me to this repo", or "create codebase docs". Do not trigger for routine feature implementation, bug fixes, or narrow code edits unless the user asks for repository-level discovery.'
license: MIT
metadata:
  source: https://github.com/github/awesome-copilot (curated import, MIT)
argument-hint: 'Optional: a focus area, e.g. "architecture only" or "testing and concerns"'
---

# Acquire Codebase Knowledge

Produce seven populated documents in `docs/codebase/` covering everything needed to
work effectively on the project. **Only document what is verifiable from files or
terminal output — never infer or assume.**

## Output contract (required)

Before finishing, all of the following must be true:

1. Exactly these files exist in `docs/codebase/`: `STACK.md`, `STRUCTURE.md`,
   `ARCHITECTURE.md`, `CONVENTIONS.md`, `INTEGRATIONS.md`, `TESTING.md`, `CONCERNS.md`.
2. Every claim is traceable to a source file, config, or terminal output.
3. Unknowns are marked `[TODO]`; intent-dependent decisions are marked `[ASK USER]`.
4. Each document includes a short "evidence" list with concrete file paths.
5. The final response lists numbered `[ASK USER]` questions and any intent-vs-reality
   divergences.

## Workflow

Copy and track this checklist:

```
- [ ] Phase 1: Run the scan, read intent documents
- [ ] Phase 2: Investigate each documentation area
- [ ] Phase 3: Populate all seven docs in docs/codebase/
- [ ] Phase 4: Validate docs, present findings, resolve all [ASK USER] items
```

### Phase 1 — Scan and read intent

1. Run the scan script from the target project root:
   ```bash
   python3 "$SKILL_ROOT/scripts/scan.py" --output docs/codebase/.codebase-scan.txt
   ```
   `$SKILL_ROOT` is the absolute path to this skill folder.
2. Search for `README`, `PRD`, `ROADMAP`, `SPEC`, `DESIGN` files and read them.
3. Summarize the stated project intent before reading any source code.

### Phase 2 — Investigate

Use the scan output to answer the questions in
[`references/inquiry-checkpoints.md`](references/inquiry-checkpoints.md). If the
stack is ambiguous, load [`references/stack-detection.md`](references/stack-detection.md).

### Phase 3 — Populate the templates

Fill the seven documents in `assets/templates/` in this order:
STACK → STRUCTURE → ARCHITECTURE → CONVENTIONS → INTEGRATIONS → TESTING → CONCERNS.
Use `[TODO]` for anything not determinable from code and `[ASK USER]` where team
intent is required.

### Phase 4 — Validate, repair, verify

For each document: confirm every non-trivial claim has an evidence reference, no
required section is empty, and unknowns use `[TODO]`. Fix and re-check until all
seven pass. Then present the summary, list every `[ASK USER]` item, and highlight
intent-vs-reality divergences from Phase 1.

## Gotchas

- **Outdated README** — it often describes intended architecture; cross-reference the
  actual file structure before treating any README claim as fact.
- **Generated output** — never document patterns from `dist/`, `build/`, `node_modules/`,
  or `__pycache__/`. Document source conventions only.
- **High-churn files** — files most present in recent git history are fragile areas;
  note them in `CONCERNS.md`.
