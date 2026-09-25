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

⏳ **Detailed plan + full technical design written — pending user review (decisions D1–D6).**

No implementation has started. Docs: `documents/initial-plan/`.
Scope note: the ≤ 300-line rule applies to **source scripts only** — plan/design documents are exempt.

## Phase Board

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Scaffold | ⬜ Not started | Blocked on D1 (language) |
| 1 | Content core | ⬜ Not started | Schemas per kind in `server/src/schema/` |
| 2 | MCP server (9 tools) | ⬜ Not started | stdio via official SDK |
| 3 | Profiles & matching | ⬜ Not started | detect + bundle; 3+ profiles |
| 4 | Client artifacts + CLI | ⬜ Not started | AGENTS.md stub, mcp.json, `agent-hq init/doctor/validate` |
| 5 | Seed content | ⬜ Not started | ~10 roles, ~6 instructions, 4 workflows, 3 conventions, 3–5 skills |
| 6 | Process enforcement (state) | ⬜ Not started | Deferrable — v1 works without it |
| 7 | Validation & docs | ⬜ Not started | E2E in CI, README/CONTRIBUTING, v1.0.0 tag |

## Open Decisions (awaiting approval)

| # | Decision | Options | Recommendation | Status |
|---|----------|---------|----------------|--------|
| D1 | Language / runtime | TypeScript vs Python | **TypeScript** (official MCP SDK, zod, single language server+CLI). Note: current `.gitignore` is the Python template — will swap if TS | ⏳ pending |
| D2 | Transport | stdio v1 vs remote HTTP | **stdio** (mcp.json template; HTTP = v2 add) | ⏳ pending |
| D3 | Repo location | this workspace vs fresh repo | **This workspace** (suggest renaming GitHub repo → `agent-hq`) | ⏳ pending |
| D4 | First validation clients | VS Code + Cline vs Claude Desktop | **VS Code + Cline** | ⏳ pending |
| D5 | Seed content sourcing | curated awesome-copilot imports + original writes | **Yes** (MIT) | ⏳ pending |
| D6 | Naming | server `agent-hq-server`, CLI `agent-hq` | Confirm or rename | ⏳ pending |

## Deliverable Checklists

### Phase 0 — Scaffold
- [ ] `server/package.json` (Node 20+, ESM) + lockfile
- [ ] `server/tsconfig.json` (strict, NodeNext)
- [ ] ESLint flat config + Prettier (incl. `max-lines` 300)
- [ ] `server/scripts/check-lines.mjs` (CI line-budget guard; docs exempt)
- [ ] vitest config + first test
- [ ] MCP SDK (pinned) + zod + yaml + glob deps
- [ ] `.github/workflows/ci.yml` (lint, typecheck, test, check:lines)
- [ ] Root README skeleton; `.gitignore` matched to stack

### Phase 1 — Content core
- [ ] `server/src/schema/` (role, instruction, skill, workflow, profile, bundle)
- [ ] `server/src/catalog/frontmatter.ts`
- [ ] `server/src/catalog/catalog.ts` (index + version digest)
- [ ] `server/src/catalog/matcher.ts` (profile pick, tag/applyTo)
- [ ] `server/src/util/` (slug, digest, result)
- [ ] Tests incl. **real awesome-copilot files** as fixtures + malformed-input tests

### Phase 2 — MCP server
- [ ] `server/src/config.ts`
- [ ] `server/src/transport/stdio.ts` (SDK isolation)
- [ ] `server/src/tools/registry.ts`
- [ ] `tools/bootstrap.ts`, `roles.ts`, `instructions.ts`, `skills.ts`, `workflows.ts`, `content-info.ts`
- [ ] `server/src/index.ts` wiring
- [ ] MCP Inspector smoke (initialize, `tools/list`, all 9 tools callable)

### Phase 3 — Profiles & matching
- [ ] `server/src/catalog/detect.ts` (stack detection)
- [ ] `server/src/catalog/bundle.ts` (onboarding bundle + size budget)
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
- [ ] `server/src/state/store.ts` (`~/.agent-hq/state/`, atomic JSON)
- [ ] `server/src/state/gates.ts` (manual / artifact / checklist-complete + ordering)
- [ ] `server/src/tools/state.ts` (`report_progress` / `get_progress`)
- [ ] Gate pass/fail/skip tests incl. tamper case

### Phase 7 — Validation & docs
- [ ] CI e2e script (JSON-RPC over stdio: initialize → bootstrap → checklist → report)
- [ ] README quickstart (< 10 min to first governed session)
- [ ] CONTRIBUTING.md + `docs/` authoring guides (content, profiles, workflows)
- [ ] v1.0.0 tag

## Change Log

| Date | Change |
|---|---|
| 2026-09-24 | Detailed plan finalized for review: `plan.md` expanded to full phase/task/acceptance detail; `technical.md` completed (was stub — now architecture, runtime flows, content schemas, tool contracts, decisions DD1–DD10, risks R1–R8); verified awesome-copilot conventions + official schemas from the live repo; 300-line rule scoped to source files only (docs exempt); decisions D5/D6 added |
| 2026-09-24 | Created `documents/initial-plan/` (plan.md, technical.md, tracking.md) — pending review |
