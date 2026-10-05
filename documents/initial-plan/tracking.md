# Agent HQ — Implementation Tracking

> Simple status board: what is implemented, what is pending.
> Companion docs: [plan.md](./plan.md) (detailed phases/tasks) · [technical.md](./technical.md) (design)
> **Last updated:** 2026-10-05

## Status Legend

| Icon | Meaning |
|---|---|
| ⬜ | Not started |
| 🚧 | In progress |
| ✅ | Done |
| ⛔ | Blocked |
| ⏳ | Pending approval / decision |

## Overall

✅ Plan approved 2026-09-24. **Phases 0–2 complete** (scaffold, content core, and MCP server over stdio). **Phase 3 in progress** (tasks 3.1–3.2 done: `detect.py` + `bundle.py`; 3.3 partial: 2 of 3 profiles shipped; 3.4 wiring + 3.5 tests outstanding). All gates green again as of 2026-10-05 (ruff · pyright · pytest 48 ✓ · check_lines) after a gate-repair pass.

Docs: `documents/initial-plan/`. Scope note: the ≤ 300-line rule applies to **source files only** — plan/design documents are exempt.

## Phase Board

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Scaffold | ✅ Done | Python/uv workspace, ruff/pyright/pytest/CI, check_lines guard |
| 1 | Content core | ✅ Done | Pydantic schemas + catalog engine; real awesome-copilot fixtures import clean |
| 2 | MCP server (9 tools) | ✅ Done | stdio via official SDK; config + transport + registry + bootstrapping + typed list/get tools |
| 3 | Profiles & matching | 🚧 In progress | 3.1 `detect.py` ✓ · 3.2 `bundle.py` ✓ · 3.3 profiles 2/3 (default missing) · 3.4 wire bootstrap → detect+bundle ✗ · 3.5 tests ✗ |
| 4 | Client artifacts + CLI | ⬜ Not started | AGENTS.md stub, mcp.json, `agent-hq init/doctor/validate` |
| 5 | Seed content | ⬜ Not started | ~10 roles, ~6 instructions, 4 workflows, 3 conventions, 3–5 skills |
| 6 | Process enforcement (state) | ⬜ Not started | Deferrable — v1 works without it |
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

### Phase 3 — Profiles & matching 🚧
- [x] `server/src/agent_hq_server/catalog/detect.py` (stack detection — manifest signals → stack tag)
- [x] `server/src/agent_hq_server/catalog/bundle.py` (onboarding bundle assembly)
- [ ] `content/profiles/` — `node-web` ✓, `python-oss` ✓, `default` ✗ (only fixture `server/tests/fixtures/content/profiles/default.profile.yaml` exists)
- [ ] Wire `bootstrap` to detect + bundle (task 3.4 — bootstrap.py still resolves inline; `bundle.py`/`detect.py` are exported but not yet called from the tool path)
- [ ] Tests: different stacks → different bundles; pinned overrides auto (task 3.5 — no tests cover detect.py/bundle.py yet)

### Phase 4 — Client artifacts + CLI
- [ ] `client/templates/AGENTS.md` (bootstrap stub, final wording)
- [ ] `client/templates/mcp.json` (VS Code + Cline)
- [ ] `client/templates/.agent-hq/profile.yaml`
- [ ] `cli/` — `init`, `doctor`, `validate`
- [ ] Real-client smoke: VS Code + Cline (D4)

### Phase 5 — Seed content
- [ ] `content/agents/` ~10 roles
- [ ] `content/instructions/` ~6
- [ ] `content/conventions/` 3 sets (typescript, node-api, python)
- [ ] `content/workflows/` 4 (standard-feature, bugfix, refactor, spike)
- [ ] `content/skills/` 3–5 (incl. acquire-codebase-knowledge import)
- [ ] `cli` — `agent-hq import <path>` (dry-run report)
- [ ] Profile→content mappings finalized

### Phase 6 — Process enforcement (deferrable)
- [ ] `server/src/agent_hq_server/state/store.py` (`~/.agent-hq/state/`, atomic JSON)
- [ ] `server/src/agent_hq_server/state/gates.py` (manual / artifact / checklist-complete + ordering)
- [ ] `server/src/agent_hq_server/tools/state.py` (`report_progress` / `get_progress`)
- [ ] Gate pass/fail/skip tests incl. tamper case

### Phase 7 — Validation & docs
- [ ] CI e2e script (JSON-RPC over stdio: initialize → bootstrap → checklist → report)
- [ ] README quickstart (< 10 min to first governed session)
- [ ] CONTRIBUTING.md + `docs/` authoring guides (content, profiles, workflows)
- [ ] v1.0.0 tag

## Change Log

| Date | Change |
|---|---|
| 2026-10-05 | **Gate repair + tracking catch-up.** Phase 3 tasks 3.1–3.2 landed at checkpoint `908b5ad` (`detect.py`, `bundle.py`, 2 profiles in `content/profiles/`) without wiring or tests — 3.4/3.5 still open. Repaired red gates from that checkpoint: ruff lint/format (unsorted imports, F401, E501, SIM105), 2 pyright errors in `test_mcp_stdio.py` reader, and a stale SDK assertion (mcp 1.30+ returns a tool-level `isError` result for unknown tools, not a JSON-RPC error — test renamed to `test_mcp_stdio_invalid_tool_is_tool_error`). All gates green; pyright run via `uvx pyright` (no node in this sandbox; CI keeps `npx -y pyright`). |
| 2026-09-26 | **Phase 2 complete.** Implemented the stdio MCP server, registry, bootstrap tool, typed content/list/get tools, and config wiring. Revalidated with `ruff`, `pyright`, pytest, and the project guard script — all green. |
| 2026-09-24 | **Phases 0–1 complete.** Scaffold: uv workspace, ruff + pyright + pytest + CI, `check_lines` guard. Content core: pydantic schemas (all 6 kinds), frontmatter parser, catalog indexer + digest, profile/glob matcher, passing tests on real awesome-copilot fixtures. All gates green |
| 2026-09-24 | **Plan approved.** D1 = Python (owner maintainability) — all docs re-pointed from TypeScript to Python: `uv` workspace, official `mcp` SDK (FastMCP), pydantic v2, ruff + pyright + pytest, `check_lines` guard. D2–D6 approved as recommended. Ready for Phase 0 |
| 2026-09-24 | Detailed plan finalized for review: `plan.md` expanded to full phase/task/acceptance detail; `technical.md` completed (was stub — now architecture, runtime flows, content schemas, tool contracts, decisions DD1–DD10, risks R1–R8); verified awesome-copilot conventions + official schemas from the live repo; 300-line rule scoped to source files only (docs exempt); decisions D5/D6 added |
| 2026-09-24 | Created `documents/initial-plan/` (plan.md, technical.md, tracking.md) — pending review |
