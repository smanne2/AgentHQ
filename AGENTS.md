# AGENTS.md — working rules for AI agents in this repo

You are working on **Agent HQ** (a centralized MCP server for agent guidance).
The approved design lives in [`documents/initial-plan/`](documents/initial-plan/).
Follow these rules in every session, without exception.

## 1. Plan before code — planning docs live in `documents/`

For **every new feature** (anything beyond a trivial fix), create the planning
documents **first**, in a dedicated folder:

```
documents/{feature-name}/
  plan.md       # goals, phasing, tasks, acceptance criteria, open decisions
  technical.md  # design: architecture, schemas/contracts, decisions, risks
  tracking.md   # status board: phase statuses, checklists, change log
```

- `{feature-name}` is a kebab-case directory name (e.g. `documents/mcp-server/`).
- The 300-line source-file rule does **not** apply to these documents.

## 2. Explicit approval gates implementation

Do **not** start implementation until the user has explicitly approved the plan
(e.g. "approved", "go ahead", "start phase N"). Silence, questions, or feedback
are **not** approval. If scope changes materially mid-implementation, stop and
get re-approval before continuing.

## 3. Update the tracking document — automatically, immediately

Whenever you complete an implementation unit (a phase, a checklist task, or any
meaningful part of one), update that feature's `tracking.md` **in the same
session** — never defer it:

- flip the completed checklist items `[ ]` → `[x]`
- update the phase-board status (⬜ / 🚧 / ✅) and the Overall section
- add a dated entry to the Change Log

A feature is not done until its tracking document reflects reality.

## Repo invariants (from the approved plan)

- Any source file ≤ 300 lines — `server/scripts/check_lines.py` enforces in CI;
  documents and content files are exempt.
- Keep the gates green after every change:
  `uv sync && uv run ruff check . && uv run ruff format --check . && npx pyright && uv run pytest && uv run python server/scripts/check_lines.py`
