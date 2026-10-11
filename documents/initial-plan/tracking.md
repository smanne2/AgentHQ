# Agent HQ — Implementation Tracking

> Simple status board: what is implemented, what is pending.
> Companion docs: [plan.md](./plan.md) (detailed phases/tasks) · [technical.md](./technical.md) (design)
> **Last updated:** 2026-10-06 (Phases 4 & 5 complete)

## Status Legend

| Icon | Meaning |
|---|---|
| ⬜ | Not started |
| 🚧 | In progress |
| ✅ | Done |
| ⛔ | Blocked |
| ⏳ | Pending approval / decision |

## Overall

✅ Plan approved 2026-09-24. **Phases 0–6 complete** (scaffold, content core, MCP server, profile-aware matching + bundle, client artifacts + CLI, seeded content tree, and process enforcement). **Phase 7 (validation & docs) is next**. Gates green: ruff · pyright · pytest · check_lines.

Docs: `documents/initial-plan/`. Scope note: the ≤ 300-line rule applies to **source files only** — plan/design documents are exempt.

## Phase Board

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Scaffold | ✅ Done | Python/uv workspace, ruff/pyright/pytest/CI, check_lines guard |
| 1 | Content core | ✅ Done | Pydantic schemas + catalog engine; real awesome-copilot fixtures import clean |
| 2 | MCP server (9 tools) | ✅ Done | stdio via official SDK; config + transport + registry + bootstrapping + typed list/get tools |
| 3 | Profiles & matching | ✅ Done | detect → pick_profile (auto) → assemble_bundle wired into bootstrap; 3 profiles; 12 Phase-3 tests; node/python/fallback/pinned all verified |
| 4 | Client artifacts + CLI | ✅ Done | Templates + `agent-hq init/doctor/validate/import`; init detects stack → writes 3 artifacts; doctor verified server-start + bundle |
| 5 | Seed content | ✅ Done | 10 roles, 9 instructions (6 + 3 conventions), 4 workflows, 4 skills, 3 profiles; all refs resolve, `validate` clean |
| 6 | Process enforcement (state) | ✅ Done | State store, gate verification, report/get progress tools and tests complete |
| 7 | Validation & docs | ⬜ Not started | E2E in CI, README/CONTRIBUTING, v1.0.0 tag |

## Open Decisions (awaiting approval)

| # | Decision | Options | Resolution (2026-09-24) | Status |
|---|----------|---------|--------------------------|--------|
| D1 | Language / runtime | TypeScript vs Python | **Python** ≥ 3.11, `uv`, official `mcp` SDK (FastMCP) + pydantic v2 — owner maintainability | ✅ decided |
| D2 | Transport | stdio v1 vs remote HTTP | **stdio** (mcp.json template; streamable-HTTP = v2 add) | ✅ approved |
| D3 | Repo location | this workspace vs fresh repo | **This workspace** — rename GitHub repo `special-telegram` → `agent-hq` | ✅ approved |
| D4 | First validation clients | VS Code + Cline vs Claude Desktop | **VS Code + Cline** (Claude Desktop as second smoke) | ✅ approved |
| D5 | Seed content sourcing | awesome-copilot imports vs original only | **Curated awesome-copilot imports + original writes** (MIT) | ✅ approved |
| D6 | Naming | — | server package `agent-hq-server`, CLI package `agent-hq` (console scripts same names) | ✅ approved |

## Deliverable Checklists

### Phase 0 — Scaffold (Python) ✅
- [x] Root `pyproject.toml` (uv workspace: server + cli) + `uv.lock`
- [x] `server/pyproject.toml` — `agent-hq-server`; deps: `mcp` (pinned), `pydantic`, `PyYAML`, `pathspec`
- [x] `cli/pyproject.toml` — `agent-hq`; `typer` + workspace dep on server
- [x] ruff (lint + format) + pyright config
- [x] `server/scripts/check_lines.py` (CI line-budget guard; docs/content excluded)
- [x] pytest config + first test
- [x] `.github/workflows/ci.yml` (ruff, pyright, pytest, check_lines)
- [x] Root README skeleton; `.gitignore` tweaks (already Python template; commit uv.lock)

### Phase 1 — Content core ✅
- [x] `server/src/agent_hq_server/schema/` (role, instruction, skill, workflow, profile, bundle — pydantic)
- [x] `server/src/agent_hq_server/catalog/frontmatter.py`
- [x] `server/src/agent_hq_server/catalog/catalog.py` (index + version digest)
- [x] `server/src/agent_hq_server/catalog/matcher.py` (profile pick, tag/applyTo)
- [x] `server/src/agent_hq_server/util/` (slug, digest, result)
- [x] Tests incl. **real awesome-copilot files** as fixtures + malformed-input tests

### Phase 2 — MCP server ✅
- [x] `server/src/agent_hq_server/config.py`
- [x] `server/src/agent_hq_server/transport/stdio.py` (FastMCP — only SDK touchpoint)
- [x] `server/src/agent_hq_server/tools/registry.py`
- [x] `tools/bootstrap.py`, `roles.py`, `instructions.py`, `skills.py`, `workflows.py`, `content_info.py`
- [x] `server/src/agent_hq_server/__main__.py` wiring
- [x] MCP smoke validation with the actual FastMCP SDK surface (`tools/list`, tool registration, and JSON-safe return handling)

### Phase 3 — Profiles & matching ✅
- [x] `server/src/agent_hq_server/catalog/detect.py` (stack detection — manifest signals → profile scoring)
- [x] `server/src/agent_hq_server/catalog/bundle.py` (onboarding bundle assembly; applyTo globs evaluated against real project files; warnings for unknown slugs / non-matching instructions)
- [x] `content/profiles/` — `node-web`, `python-oss`, `default` (mirrored in fixtures)
- [x] Wire `bootstrap` to detect + bundle (task 3.4 — pin file > explicit arg > `detect_stack` signals → `pick_profile` → `assemble_bundle`; inline phase-2 resolution removed)
- [x] Tests: different stacks → different bundles; pinned overrides auto; fallback when undetectable (task 3.5 — `server/tests/test_bundle.py`, 12 tests incl. glob matching + vendor-dir pruning)

### Phase 4 — Client artifacts + CLI ✅
- [x] `client/templates/AGENTS.md` (bootstrap stub — exact technical.md §3.1 wording + detected stack/profile)
- [x] `client/templates/mcp.json` (stdio: `uv run agent-hq-server` + `AGENT_HQ_CONTENT` env; `init` fills real paths)
- [x] `client/templates/.agent-hq/profile.yaml` (editable pin, stack pre-filled by detection)
- [x] `cli/` — `init` (detects stack → writes 3 artifacts), `doctor` (server starts + content loads + non-empty bundle), `validate` (schema-checks tree)
- [x] `cli` — `import` (5.7): dry-run report + `--copy` verbatim copy
- [ ] Real-client smoke: VS Code + Cline (D4) — *manual step; documented in README, needs a live client*

### Phase 5 — Seed content ✅
- [x] `content/agents/` — 10 roles (architect, engineer, code-reviewer, security-reviewer, test-engineer, docs-writer, refactorer, perf-analyst, api-designer, a11y-reviewer)
- [x] `content/instructions/` — 6 (git-hygiene, agent-safety, testing-discipline, code-style-generic, doc-updates, commit-messages)
- [x] `content/conventions/` — 3 (typescript, node-api, python) as tagged instructions
- [x] `content/workflows/` — 4 (standard-feature, bugfix, refactor, spike) with phases/checklists/gates
- [x] `content/skills/` — 4 (acquire-codebase-knowledge import + working scan.py/references/templates, adr-writer, test-plan, pre-commit-check)
- [x] `cli` — `agent-hq import <path>` (dry-run report)
- [x] Profile→content mappings finalized (all profile slugs resolve; `validate` clean)

### Phase 6 — Process enforcement (deferrable) ✅
- [x] `server/src/agent_hq_server/state/store.py` (`~/.agent-hq/state/`, atomic JSON)
- [x] `server/src/agent_hq_server/state/gates.py` (manual / artifact / checklist-complete + ordering)
- [x] `server/src/agent_hq_server/tools/state.py` (`report_progress` / `get_progress`)
- [x] Tests: gate pass/fail/skip tests incl. tamper case

### Phase 7 — Validation & docs
- [ ] CI e2e script (JSON-RPC over stdio: initialize → bootstrap → checklist → report)
- [ ] README quickstart (< 10 min to first governed session)
- [ ] CONTRIBUTING.md + `docs/` authoring guides (content, profiles, workflows)
- [ ] v1.0.0 tag

## Change Log

| Date | Change |
|---|---|
| 2026-10-06 | **Phases 4 & 5 complete.** Phase 4: `client/templates/` (AGENTS.md stub per §3.1, mcp.json, profile.yaml pin) + CLI `init`/`doctor`/`validate`/`import` (one module each in `cli/src/agent_hq_cli/`). `init` detects stack via the server matcher and writes all three artifacts with real paths; `doctor` spawns the real stdio server and verifies a non-empty bundle (verified: node project → node-web profile, server starts). Phase 5: seeded `content/` — 10 roles, 9 instructions (incl. 3 conventions), 4 workflows, 4 skills (acquire-codebase-knowledge imported with a working `scan.py` + references + 7 templates), and 3 profiles reconciled to the real slugs. `agent-hq validate` is clean; every profile→content ref resolves. |
| 2026-10-05 | **Phase 3 complete.** Wired `bootstrap` to the Phase-3 pipeline (task 3.4): `detect_stack` manifest signals → `pick_profile` auto-match → `assemble_bundle` (rewritten: `source` param, warnings for unknown slugs, applyTo globs evaluated against a pruned scan of the project's file paths). Added `content/profiles/default.profile.yaml` (3.3) and `server/tests/test_bundle.py` — 12 tests: node vs python → different bundles, undetectable → fallback, pin file / explicit arg override detection, glob instructions require matching project files, vendor-dir pruning, ErrorView when no profiles (3.5). Removed dead `detect_stack_from_signals` + unused `BundleMatchInput`. All gates green (pytest 60). |
| 2026-10-05 | **Gate repair + tracking catch-up.** Phase 3 tasks 3.1–3.2 landed at checkpoint `908b5ad` (`detect.py`, `bundle.py`, 2 profiles in `content/profiles/`) without wiring or tests — 3.4/3.5 still open. Repaired red gates from that checkpoint: ruff lint/format (unsorted imports, F401, E501, SIM105), 2 pyright errors in `test_mcp_stdio.py` reader, and a stale SDK assertion (mcp 1.30+ returns a tool-level `isError` result for unknown tools, not a JSON-RPC error — test renamed to `test_mcp_stdio_invalid_tool_is_tool_error`). All gates green; pyright run via `uvx pyright` (no node in this sandbox; CI keeps `npx -y pyright`). |
| 2026-09-26 | **Phase 2 complete.** Implemented the stdio MCP server, registry, bootstrap tool, typed content/list/get tools, and config wiring. Revalidated with `ruff`, `pyright`, pytest, and the project guard script — all green. |
| 2026-09-24 | **Phases 0–1 complete.** Scaffold: uv workspace, ruff + pyright + pytest + CI, `check_lines` guard. Content core: pydantic schemas (all 6 kinds), frontmatter parser, catalog indexer + digest, profile/glob matcher, passing tests on real awesome-copilot fixtures. All gates green |
| 2026-09-24 | **Plan approved.** D1 = Python (owner maintainability) — all docs re-pointed from TypeScript to Python: `uv` workspace, official `mcp` SDK (FastMCP), pydantic v2, ruff + pyright + pytest, `check_lines` guard. D2–D6 approved as recommended. Ready for Phase 0 |
| 2026-09-24 | Detailed plan finalized for review: `plan.md` expanded to full phase/task/acceptance detail; `technical.md` completed (was stub — now architecture, runtime flows, content schemas, tool contracts, decisions DD1–DD10, risks R1–R8); verified awesome-copilot conventions + official schemas from the live repo; 300-line rule scoped to source files only (docs exempt); decisions D5/D6 added |
| 2026-09-24 | Created `documents/initial-plan/` (plan.md, technical.md, tracking.md) — pending review |
