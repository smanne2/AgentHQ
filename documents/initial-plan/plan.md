# Agent HQ — Implementation Plan

> **Feature:** Centralized MCP server that broadcasts agent roles, instructions, skills, and standardized workflows.
> **Status:** ⏳ **Pending review** — no implementation has started.
> **Companion docs:** [technical.md](./technical.md) (design, schemas, tool contracts, decisions, risks) · [tracking.md](./tracking.md) (status board)
> **Last updated:** 2026-09-24

---

## 1. Overview

**Agent HQ** (working name) is a centralized Model Context Protocol (MCP) server that acts as the single source of truth for how coding agents behave. Any agent client (VS Code Copilot, Cline, Claude Desktop, or any MCP-capable client) connects to the server and pulls exactly the guidance it needs for a given project:

- **Roles** — who the agent is (e.g. "Architect", "Security Reviewer")
- **Instructions** — standing rules (code style, git hygiene, agent safety)
- **Skills** — reusable task playbooks (e.g. "map this codebase")
- **Workflows** — standardized, phased development processes with checklists and gates
- **Conventions** — stack-specific rules (TypeScript, Node API, Python, …)

**Result:** every new project starts from the same roles, conventions, and process — development stops being vague.

Content files follow the [awesome-copilot](https://github.com/github/awesome-copilot) conventions (MIT-licensed): `*.agent.md`, `*.instructions.md`, `skills/<name>/SKILL.md` — so existing community content imports with zero rework. (Verified 2026-09: the repo publishes these conventions plus official JSON schemas for collections.)

### Code size rule (from original brief)

1. Implementation must be **modular** — one concern per module.
2. Everything is **grouped logically** — by content kind, tool, transport, etc.
3. **Any source file (script) ≤ 300 lines** — enforced in CI (`pnpm check:lines`). *Documents (markdown/YAML) are exempt from this rule.*

---

## 2. Goals / Non-Goals

### Goals

| # | Goal |
|---|------|
| G1 | Single source of truth, version-controlled in git |
| G2 | Identical guidance for every project and every agent client |
| G3 | Standardized process: phased workflow with explicit checklists and gates |
| G4 | Content is plain markdown / YAML — reviewable, diffable, importable |
| G5 | Token-efficient delivery (progressive disclosure: `list_*` = slugs, `get_*` = full) |
| G6 | Modular code, logical grouping, ≤ 300 lines per **source file** (docs exempt) |

### Non-Goals (v1)

- No LLM inference inside the server (it is a content service, not an agent)
- No multi-tenant admin dashboard / web UI
- No authentication / authorization (single-user local trust model — v2 topic)
- No push into agent system prompts (MCP is pull-based — see §3)

---

## 3. How Consistency Works (Bootstrap Handshake)

MCP servers cannot inject content into an agent's system prompt. Consistency is therefore achieved with a **pull-based bootstrap handshake**:

1. Every new project ships with a tiny `AGENTS.md` stub: *"First action of any session: call `agent_hq.bootstrap` with the project path. Follow the returned workflow. Consult `agent_hq.*` tools before doing work."*
2. The server matches the project (pinned profile file + stack auto-detection) against `content/profiles/` and returns an **onboarding bundle**: default workflow (phases + checklists + gates), matched instructions, role roster, skill list, content version digest.
3. During development the agent calls on-demand tools (`get_role`, `get_skill`, `get_instructions`, `get_checklist`, …).
4. The agent reports phase progress (`report_progress`); the server tracks state and **flags skipped phases / failed gates** — making the process enforceable, not just advisory.

Full diagrams, matching rules, and tool contracts: [technical.md](./technical.md).

---

## 4. Architecture

```
[VS Code Copilot / Cline / Claude / any MCP client]
        │   stdio (v1) · streamable HTTP (v2, optional)
        ▼
┌─────────────────────────────────────────────┐
│            MCP SERVER ("agent-hq")          │
│  transport/  stdio adapter (SDK isolation)  │
│  tools/      bootstrap · roles ·            │
│              instructions · skills ·        │
│              workflows · state              │
│  catalog/    frontmatter parser, index,     │
│              matcher (profile/glob/tag)     │
│  state/      progress + gates (phase 6)     │
└─────────────────────────────────────────────┘
        ▲ reads content/      ▲ matches against project profile
        │                    │ (.agent-hq/profile.yaml + manifest files)
   content/ (git repo)        target project (AGENTS.md stub + profile)
```

The server contains **zero LLM logic** — it is a typed content service over a git-versioned content tree. Full module map with per-file line budgets: [technical.md §2](./technical.md#2-architecture).

---

## 5. Detailed Implementation Plan (phases → tasks → acceptance)

Phases are sequenced so each ends in something demonstrable. Dependency chain: **0 → 1 → 2 → 3 → 4 → 5 → 7**, with **6** deferrable (slotted between 5 and 7).

---

### Phase 0 — Scaffold

**Goal:** a building, testing, linting skeleton where every later phase is "add modules".

| # | Task |
|---|------|
| 0.1 | `server/package.json` — Node 20+, ESM, scripts: `dev`, `build`, `test`, `lint`, `check:lines`, `start` |
| 0.2 | `server/tsconfig.json` — strict, ESM, `NodeNext` resolution |
| 0.3 | ESLint (flat config) + Prettier, incl. `max-lines` = 300 rule (warn now, error in CI) |
| 0.4 | `scripts/check-lines.mjs` — fails CI if any source file > 300 lines (docs excluded) |
| 0.5 | vitest config + first trivial test green |
| 0.6 | Deps: `@modelcontextprotocol/sdk` (pinned), `zod`, `yaml`, `glob`/`micromatch` |
| 0.7 | `.github/workflows/ci.yml` — lint, typecheck, test, `check:lines` |
| 0.8 | Repo root: `README.md` (project intro + quickstart skeleton), fix `.gitignore` to match chosen stack |

**Acceptance:** `pnpm install && pnpm lint && pnpm test && pnpm check:lines` all green; `server/src/index.ts` stub starts and exits cleanly.

**Blocked on:** decision D1 (language). If Python is chosen, 0.1–0.8 map 1:1 to `pyproject.toml`/ruff/pyright/pytest equivalents.

---

### Phase 1 — Content Core (no MCP yet)

**Goal:** the content engine: parse, index, validate, match. Testable standalone — this is where awesome-copilot compatibility lives.

| # | Task |
|---|------|
| 1.1 | `server/src/schema/role.ts` · `instruction.ts` · `skill.ts` · `workflow.ts` · `profile.ts` · `bundle.ts` — zod schemas per content kind (see technical.md §4) |
| 1.2 | `server/src/catalog/frontmatter.ts` — split `---` fences, YAML parse, validate against kind schema, tolerate unknown keys |
| 1.3 | `server/src/catalog/catalog.ts` — walk `content/`, kind by path pattern, build in-memory index + content version digest |
| 1.4 | `server/src/catalog/matcher.ts` — profile matching: pinned > auto-detect (manifest signals) > fallback; tag/glob matching for instructions |
| 1.5 | Fixture tests: **real awesome-copilot files** downloaded at implementation time (≥3 agents, ≥3 instructions, ≥2 skills) pinned as test fixtures — import-with-zero-rework is proven by tests |
| 1.6 | Negative tests: malformed frontmatter → clear error with file path (never crashes the index build) |

**Acceptance:** `pnpm test` green incl. awesome-copilot fixtures; catalog index for a sample tree loads < 100 ms.

---

### Phase 2 — MCP Server

**Goal:** the content engine exposed over MCP stdio, callable from any client.

| # | Task |
|---|------|
| 2.1 | `server/src/config.ts` — env/flags: `AGENT_HQ_CONTENT` path, project path defaults |
| 2.2 | `server/src/transport/stdio.ts` — SDK isolation layer (the only file touching `@modelcontextprotocol/sdk` transport) |
| 2.3 | `server/src/tools/registry.ts` — assembles all tool handlers onto one server instance |
| 2.4 | `tools/bootstrap.ts` — `agent_hq.bootstrap` (bundle assembly lives in `catalog/bundle.ts`, phase 3) |
| 2.5 | `tools/roles.ts` — `list_roles` / `get_role` |
| 2.6 | `tools/instructions.ts` — `list_instructions` / `get_instruction` |
| 2.7 | `tools/skills.ts` — `list_skills` / `get_skill` (incl. sibling-file manifest for skill dirs) |
| 2.8 | `tools/workflows.ts` — `list_workflows` / `get_workflow` / `get_checklist` |
| 2.9 | `tools/content-info.ts` — `agent_hq.content_info` (version digest, counts) |
| 2.10 | `server/src/index.ts` — wire config → catalog → registry → transport |
| 2.11 | MCP Inspector smoke: initialize, `tools/list` shows all 9 tools, each callable, Inspector round-trips |

**Acceptance:** Inspector session exercises every tool against the sample content tree; all responses typed (zod-validated) and human-readable.

---

### Phase 3 — Profiles & Matching

**Goal:** the *right* content for *this* project — the heart of "consistent implementation".

| # | Task |
|---|------|
| 3.1 | `server/src/catalog/detect.ts` — stack detection: `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` / … signals → stack tags |
| 3.2 | `server/src/catalog/bundle.ts` — assemble onboarding bundle: profile → workflow + phases, instructions (applyTo match), role roster, skill list, version digest |
| 3.3 | `content/profiles/` — 3+ profiles: `node-web`, `python-oss`, `default` (each a small YAML, see technical.md §4.5) |
| 3.4 | Wire `bootstrap` to detect + bundle (replaces phase-2 stub behavior) |
| 3.5 | Tests: fixture trees for different stacks → assert *different* bundles; pinned profile overrides detection; fallback when undetectable |

**Acceptance:** bootstrap on a Node tree vs a Python tree returns visibly different instructions/conventions; every run returns a `nextAction` string the agent can act on.

---

### Phase 4 — Client Artifacts + CLI

**Goal:** a new project is one command from "agent is governed": `agent-hq init`.

| # | Task |
|---|------|
| 4.1 | `client/templates/AGENTS.md` — bootstrap stub (exact wording in technical.md §3.1) |
| 4.2 | `client/templates/mcp.json` — VS Code + Cline server config (stdio command + `AGENT_HQ_CONTENT` env) |
| 4.3 | `client/templates/.agent-hq/profile.yaml` — editable pin (stack pre-filled by detection) |
| 4.4 | `cli/` package — `agent-hq init <dir>` (writes 4.1–4.3, detects stack) |
| 4.5 | `cli/` — `agent-hq doctor` (server starts, content loads, bundle non-empty) |
| 4.6 | `cli/` — `agent-hq validate` (schema-check whole content tree; contributor gate) |
| 4.7 | **Real-client smoke:** VS Code + Cline on a throwaway project → observe bootstrap call, verify agent follows the workflow (decision D4) |

**Acceptance:** `agent-hq init demo && agent-hq doctor` green; in VS Code *and* Cline the agent demonstrably calls `bootstrap` first and cites returned workflow phases.

---

### Phase 5 — Seed Content

**Goal:** the content tree is actually useful on day one. Curated from awesome-copilot (MIT) + original Agent HQ content.

| # | Task |
|---|------|
| 5.1 | `content/agents/` — ~10 roles: architect, engineer, code-reviewer, security-reviewer, test-engineer, docs-writer, refactorer, perf-analyst, api-designer, a11y-reviewer (import + trim) |
| 5.2 | `content/instructions/` — ~6: git-hygiene, agent-safety, testing-discipline, code-style-generic, doc-updates, commit-messages |
| 5.3 | `content/conventions/` — 3 sets: typescript, node-api, python (these are instructions with `stack` tags — see DD5) |
| 5.4 | `content/workflows/` — 4: `standard-feature`, `bugfix`, `refactor`, `spike` (phases + checklists + gates, technical.md §4.4) |
| 5.5 | `content/skills/` — 3–5: acquire-codebase-knowledge (import), adr-writer, test-plan, pre-commit-check |
| 5.6 | `content/profiles/` — finalize profile→content mappings for the seed set |
| 5.7 | `cli` — `agent-hq import <path>` — copy awesome-copilot files in with a dry-run report (normalizes nothing if schemas already accept) |

**Acceptance:** `agent-hq validate` green; a fresh `init`-ed project bootstraps into a complete, coherent bundle (workflow + 4–8 instructions + roster).

---

### Phase 6 — Process Enforcement (deferrable)

**Goal:** the process is a checkable contract, not a suggestion. (Can ship v1 without it; everything above still works — enforcement then relies on the AGENTS.md stub's instructions.)

| # | Task |
|---|------|
| 6.1 | `server/src/state/store.ts` — JSON persistence under `~/.agent-hq/state/<project-hash>-<workflow>.json` |
| 6.2 | `server/src/state/gates.ts` — gate verification: `manual` (requires `approved: true` evidence), `artifact` (glob exists in project), `checklist-complete`, `none`; ordering enforcement (no phase N+1 start before gate N passes) |
| 6.3 | `tools/state.ts` — `agent_hq.report_progress` + `agent_hq.get_progress` |
| 6.4 | Tests: gate pass/fail/skip matrix; tamper (report phase 3 without 1–2) → flagged |

**Acceptance:** a client that skips a phase receives explicit flags from `report_progress`/`get_progress` naming what failed.

---

### Phase 7 — Validation & Docs

**Goal:** provable end-to-end behavior + maintainability for future contributors.

| # | Task |
|---|------|
| 7.1 | E2E smoke script: spawn real stdio server, JSON-RPC `initialize` → `bootstrap` (fixture project) → `get_checklist` → `report_progress` sequence — runs in CI |
| 7.2 | `README.md` — full quickstart (init → client config → first governed session) |
| 7.3 | `CONTRIBUTING.md` — how to add/modify content (schemas, validate, PR), for the content side |
| 7.4 | `docs/` — one-pagers: content authoring guide, profile authoring guide, workflows & gates guide |
| 7.5 | Tag v1.0.0 |

**Acceptance:** CI green on the full suite (unit + e2e); a stranger can follow README to a governed session in < 10 minutes.

---

## 6. Validation Strategy (summary)

| Layer | What | Tooling |
|---|---|---|
| Unit | frontmatter parse, schemas, matcher, bundle, gates | vitest + real awesome-copilot fixtures |
| Integration | catalog build over full content tree | vitest |
| MCP protocol | Inspector (manual) + JSON-RPC stdio e2e (automated, CI) | MCP Inspector · spawn script |
| Real clients | VS Code + Cline smoke (D4) | manual checklist, documented in README |
| Content quality | schema validation of entire tree | `agent-hq validate` (also CI) |
| Code discipline | 300-line rule, lint, types | `check:lines` · ESLint · tsc |

---

## 7. Open Decisions (your call)

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| **D1** | Language / runtime | TypeScript vs Python | **TypeScript** — official MCP TS SDK is the reference implementation; zod covers both content + tool schemas; single language for server *and* CLI. Note: current `.gitignore` is the Python template — we'll swap it if TS is chosen. (Python `mcp`/FastMCP is a fully workable alternative; module map is 1:1.) |
| **D2** | Transport | stdio v1 vs remote HTTP | **stdio** for v1 — zero client config friction (mcp.json template). Streamable-HTTP adapter is a v2 add; transport is isolated so it's cheap later. |
| **D3** | Repo location | this workspace vs fresh repo | **This workspace** — docs + MIT license already here; it's otherwise empty. Suggest renaming the GitHub repo to `agent-hq` (one click, no code impact). |
| **D4** | First validation clients | VS Code + Cline vs Claude Desktop | **VS Code + Cline** — both consume `mcp.json`-style stdio config and are common agent workbenches; Claude Desktop as second smoke. |
| **D5** | Seed content sourcing | import curated awesome-copilot subset + original writes | **Yes to both** — MIT license permits; keeps day-one content high-quality. |
| **D6** | Naming | package `agent-hq`, server binary `agent-hq-server`, CLI `agent-hq` | Confirm or rename. |

---

## 8. v2 Ideas (parked, not planned)

- Streamable-HTTP transport for remote/shared servers + auth
- Cross-project memory: `learnings/` content kind (project A's lessons served to project B)
- `search` tool (keyword/semantic-ish ranking over content)
- SQLite state backend; multi-user server
- Distribution to npm / PyPI
- MCP *resources* (content as resources, not only tools) for clients that prefer that surface
- Web dashboard read-only view of state + catalog

---

*Detailed design — component diagram, runtime flows, content schemas, tool contracts, design decisions, risks — is in [technical.md](./technical.md). Live status: [tracking.md](./tracking.md).*
