# Agent HQ — Implementation Tracking

> Simple status board: what is implemented, what is pending.
> Companion docs: [plan.md](./plan.md) (detailed phases/tasks) · [technical.md](./technical.md) (design)
> **Last updated:** 2026-09-24

## Status Legend

| Icon | Meaning |
|---|---|
| ⬜ | Not started |
| 🚧 | In progress |
| ✅ | Done |
| ⛔ | Blocked |
| ⏳ | Pending approval / decision |

## Overall

✅ **Plan approved 2026-09-24 — ready for implementation.** D1 = **Python** (maintainability); D2–D6 as recommended. No code written yet — **Phase 0 (scaffold) is next.**

Docs: `documents/initial-plan/`. Scope note: the ≤ 300-line rule applies to **source files only** — plan/design documents are exempt.

## Phase Board

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Scaffold | ⬜ Not started | **Ready** — D1 resolved (Python/uv); next up |
| 1 | Content core | ⬜ Not started | Pydantic models in `server/src/agent_hq_server/schema/` |
| 2 | MCP server (9 tools) | ⬜ Not started | stdio via official SDK |
| 3 | Profiles & matching | ⬜ Not started | detect + bundle; 3+ profiles |
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

### Phase 0 — Scaffold (Python)
- [ ] Root `pyproject.toml` (uv workspace: server + cli) + `uv.lock`
- [ ] `server/pyproject.toml` — `agent-hq-server`; deps: `mcp` (pinned), `pydantic`, `PyYAML`, `pathspec`
- [ ] `cli/pyproject.toml` — `agent-hq`; `typer` + workspace dep on server
- [ ] ruff (lint + format) + pyright config
- [ ] `server/scripts/check_lines.py` (CI line-budget guard; docs/content excluded)
- [ ] pytest config + first test
- [ ] `.github/workflows/ci.yml` (ruff, pyright, pytest, check_lines)
- [ ] Root README skeleton; `.gitignore` tweaks (already Python template; commit uv.lock)

### Phase 1 — Content core
- [ ] `server/src/agent_hq_server/schema/` (role, instruction, skill, workflow, profile, bundle — pydantic)
- [ ] `server/src/agent_hq_server/catalog/frontmatter.py`
- [ ] `server/src/agent_hq_server/catalog/catalog.py` (index + version digest)
- [ ] `server/src/agent_hq_server/catalog/matcher.py` (profile pick, tag/applyTo)
- [ ] `server/src/agent_hq_server/util/` (slug, digest, result)
- [ ] Tests incl. **real awesome-copilot files** as fixtures + malformed-input tests

### Phase 2 — MCP server
- [ ] `server/src/agent_hq_server/config.py`
- [ ] `server/src/agent_hq_server/transport/stdio.py` (FastMCP — only SDK touchpoint)
- [ ] `server/src/agent_hq_server/tools/registry.py`
- [ ] `tools/bootstrap.py`, `roles.py`, `instructions.py`, `skills.py`, `workflows.py`, `content_info.py`
- [ ] `server/src/agent_hq_server/__main__.py` wiring
- [ ] MCP Inspector smoke (initialize, `tools/list`, all 9 tools callable)

### Phase 3 — Profiles & matching
- [ ] `server/src/agent_hq_server/catalog/detect.py` (stack detection)
- [ ] `server/src/agent_hq_server/catalog/bundle.py` (onboarding bundle + size budget)
- [ ] `content/profiles/` — `node-web`, `python-oss`, `default`
- [ ] Tests: different stacks → different bundles; pinned overrides auto

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
| 2026-09-24 | **Plan approved.** D1 = Python (owner maintainability) — all docs re-pointed from TypeScript to Python: `uv` workspace, official `mcp` SDK (FastMCP), pydantic v2, ruff + pyright + pytest, `check_lines` guard. D2–D6 approved as recommended. Ready for Phase 0 |
| 2026-09-24 | Detailed plan finalized for review: `plan.md` expanded to full phase/task/acceptance detail; `technical.md` completed (was stub — now architecture, runtime flows, content schemas, tool contracts, decisions DD1–DD10, risks R1–R8); verified awesome-copilot conventions + official schemas from the live repo; 300-line rule scoped to source files only (docs exempt); decisions D5/D6 added |
| 2026-09-24 | Created `documents/initial-plan/` (plan.md, technical.md, tracking.md) — pending review |
