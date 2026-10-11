# Agent HQ — Technical Design

> Companion to [plan.md](./plan.md) (what & when). This document covers **why & how**: value, architecture, runtime flows, content schemas, tool contracts, design decisions, risks.
> **Status:** ✅ Approved 2026-09-24 — D1 = Python
> **Last updated:** 2026-09-24

---

## 1. Problem & Value

### 1.1 The problem

Starting a new project with a coding agent today means:

| Pain | Symptom |
|---|---|
| Duplicated guidance | Every project re-writes `AGENTS.md` / `.cursorrules` / prompt files from scratch → rules drift project to project |
| Free-form process | The agent invents its own approach each session — the "vague development" this project exists to eliminate |
| Ad-hoc roles | Specialist personas defined per project, with inconsistent tool access and boundaries |
| No cross-project memory | A lesson learned in project A is not available in project B |
| No enforcement | Nothing stops the agent from skipping tests, security review, or committing straight to `main` |

### 1.2 What Agent HQ adds

| Value | Mechanism |
|---|---|
| **Consistent implementation** | One git-tracked content tree; every project and every client resolves the same roles, conventions, and instructions |
| **Standardized process** | Phased workflows with checklists + gates; the server tracks progress and flags skipped phases |
| **Zero duplication** | Update a rule once in `content/` → all projects pick it up on their next session |
| **Instant onboarding** | `agent-hq init` scaffolds a new project with a bootstrap stub + profile; the agent is productive from session one |
| **Reviewable governance** | All guidance is markdown in git → PR review, history, blame; awesome-copilot community content imports directly |
| **Token efficiency** | Progressive disclosure: `list_*` returns slugs, `get_*` returns full content on demand |
| **Client-agnostic** | Any MCP client (VS Code, Cline, Claude, …) works — no per-client prompt re-authoring |
| **Enforceable, not advisory** | Progress tracking + workflow gates turn "follow the process" from a suggestion into a checkable contract |

---

## 2. Architecture

### 2.1 Components & dependency rules

```
                ┌──────────── client (MCP) ────────────┐
                │                                      │
                ▼                                      │ JSON-RPC (stdio)
        ┌────────────────┐                    ┌────────────────────┐
        │  transport/    │◄───────────────────│  tools/            │
        │  stdio.py      │   handlers         │  bootstrap, roles, │
        └───────┬────────┘                    │  instructions, …   │
                │                             └───────┬────────────┘
                │                                     │
        ┌───────▼─────────────────────────────────────▼─────┐
        │                      catalog/                     │
        │  frontmatter · catalog · matcher · detect · bundle│
        └───────┬─────────────────────────────┬─────────────┘
                │ reads                       │ matches against
        ┌───────▼─────────┐          ┌────────▼──────────────┐
        │  content/       │          │  state/               │
        │  (git markdown) │          │  store · gates (P6)   │
        └─────────────────┘          └────────┬──────────────┘
                                              │ JSON files
                                     ┌────────▼────────────┐
                                     │ ~/.agent-hq/state/  │
                                     └─────────────────────┘
```

**Dependency rule (enforced by lint boundary checks where available):**
`transport → tools → catalog / state → config`. Nothing below `tools/` imports from `tools/`; nothing imports the `mcp` SDK except `transport/stdio.py` and `tools/registry.py`. This keeps the content engine independently testable and swappable.

### 2.2 Repository layout (monorepo, decision D3 · Python per D1)

```
agent-hq/                                  # monorepo, uv workspace (D3: this repo · D1: Python)
├── pyproject.toml                        # root: uv workspace members [server, cli]; uv.lock committed
├── server/                               # package "agent-hq-server" (console script: agent-hq-server)
│   ├── pyproject.toml                    # deps: mcp (pinned) · pydantic v2 · PyYAML · pathspec
│   ├── src/agent_hq_server/
│   │   ├── __init__.py                   # package + version                                  (~10)
│   │   ├── __main__.py                   # entry: config → catalog → registry → transport     (~20)
│   │   ├── config.py                     # env/flags: AGENT_HQ_CONTENT, paths                 (~80)
│   │   ├── schema/                       # pydantic models, one module per content kind
│   │   │   ├── __init__.py               # re-exports + shared bits                           (~30)
│   │   │   ├── role.py                   #                                                    (~80)
│   │   │   ├── instruction.py            # (conventions reuse it)                             (~90)
│   │   │   ├── skill.py                  #                                                    (~80)
│   │   │   ├── workflow.py               # phases, checklists, gates                          (~140)
│   │   │   ├── profile.py                # profile.yaml + matching rules                      (~120)
│   │   │   └── bundle.py                 # bootstrap return shape                             (~90)
│   │   ├── catalog/
│   │   │   ├── __init__.py               #                                                    (~10)
│   │   │   ├── frontmatter.py            # fence split + YAML + validate                      (~140)
│   │   │   ├── catalog.py                # tree walk → index + version digest                 (~130)
│   │   │   ├── matcher.py                # profile pick, tag/applyTo matching                 (~150)
│   │   │   ├── detect.py                 # stack detection from manifest files                (~120)  [P3]
│   │   │   └── bundle.py                 # onboarding bundle assembly                         (~120)  [P3]
│   │   ├── tools/
│   │   │   ├── __init__.py               # re-exports                                         (~10)
│   │   │   ├── registry.py               # attaches all handlers to FastMCP instance          (~90)
│   │   │   ├── bootstrap.py              #                                                    (~80)
│   │   │   ├── roles.py                  # list_roles / get_role                              (~80)
│   │   │   ├── instructions.py           # list/get                                           (~90)
│   │   │   ├── skills.py                 # list/get + sibling manifest                        (~100)
│   │   │   ├── workflows.py              # list / get / get_checklist                         (~110)
│   │   │   ├── content_info.py           # version + counts                                   (~50)
│   │   │   └── state.py                  # report_progress / get_progress                     (~120)  [P6]
│   │   ├── transport/
│   │   │   └── stdio.py                  # FastMCP wiring — only `mcp` SDK touchpoint         (~70)
│   │   ├── state/
│   │   │   ├── store.py                  # JSON persistence, atomic write                     (~120)  [P6]
│   │   │   └── gates.py                  # gate verification + ordering                       (~130)  [P6]
│   │   └── util/
│   │       ├── slug.py                   # filename → slug, uniqueness                        (~50)
│   │       ├── digest.py                 # content tree hash                                  (~60)
│   │       └── result.py                 # typed error/ok helpers                             (~50)
│   ├── tests/                            # mirrors src/; fixtures/ holds real awesome-copilot files
│   └── scripts/check_lines.py            # 300-line CI guard                                  (~40)
├── cli/                                  # package "agent-hq" (typer; console script: agent-hq)
│   ├── pyproject.toml                    # deps: typer + workspace dep on agent-hq-server
│   └── src/agent_hq_cli/                 # main · init · doctor · validate · import_cmd · list_cmd  (~50–120 ea)
├── client/
│   └── templates/                        # AGENTS.md · mcp.json (uv run) · .agent-hq/profile.yaml
├── content/                             # THE content tree (git-versioned)
│   ├── agents/*.agent.md
│   ├── instructions/*.instructions.md
│   ├── conventions/*.instructions.md
│   ├── skills/<name>/SKILL.md            (+ optional scripts/, references/)
│   ├── workflows/*.workflow.md
│   └── profiles/*.profile.yaml
├── .github/workflows/ci.yml              # ruff · pyright · pytest · check_lines · content validate
└── LICENSE (MIT) · README.md · CONTRIBUTING.md · docs/
```

Parentheticals are target line counts — all comfortably under the 300-line source-file rule, and the budget is checked in CI. (Documents such as this file are exempt.)

---

## 3. Runtime Flows

### 3.1 Bootstrap handshake (session start)

```
client                 agent-hq server                project dir
  │                        │                              │
  │ spawn (stdio)          │                              │
  │────initialize──────────►                              │
  │◄────────────────ok────────                            │
  │                                                        │
  │  agent reads AGENTS.md stub:                           │
  │  "first action: call agent_hq.bootstrap"               │
  │                                                        │
  │────tools/call bootstrap {projectPath, hints?}────────► │
  │                        │ 1. read .agent-hq/profile.yaml├─── (if pinned)
  │                        │ 2. else detect stack          ├─── package.json, …
  │                        │ 3. pick profile (matcher)     │
  │                        │ 4. assemble bundle            │
  │◄──────────────── Bundle (JSON)                         │
  │                                                        │
  │ agent: "follow workflow W, start at phase 1"           │
```

**AGENTS.md stub (the exact shipped text):**

```markdown
# Agent HQ — bootstrap required

Before ANY work in this project:

1. Call `agent_hq.bootstrap` with `{"projectPath": "<this project's absolute path>"}`.
2. Follow the returned workflow: phases in order, one at a time.
3. At each phase start, call `agent_hq.get_checklist` for that phase;
   consult the returned roles / instructions / skills before acting.
4. At each phase end, call `agent_hq.report_progress` with completed
   checklist indices and evidence. If the response flags a failed gate,
   stop and surface it to the user.
5. Never skip or reorder phases. If you must deviate, ask the user first
   and record the deviation in your report.

Project profile (pinned content): `.agent-hq/profile.yaml`
```

### 3.2 On-demand retrieval (during work)

Agent hits a decision point → picks from the roster/list returned at bootstrap → `get_role` / `get_skill` / `get_instruction` / `get_workflow(phase)` → full markdown. Server is stateless here (content cache in memory, rebuilt on startup).

### 3.3 Progress & gates (phase 6)

```
agent: report_progress {workflow, phase: "design", completed: [0,1,2], evidence: "docs/design/api.md"}
server: 1. load state (per project+workflow)
         2. verify ordering (all prior gates passed?)
         3. verify this phase's gate:
              manual   → requires approved:true
              artifact → glob pattern must exist in projectPath
              checklist→ all indices reported complete
         4. persist, return {ok|flags[], nextPhase}
```

Flags are *advisory-but-visible*: the AGENTS.md stub instructs the agent to stop on flags. The server never blocks tool calls (it cannot) but makes every deviation loud and inspectable via `get_progress`.

---

## 4. Content Schemas

All markdown content = YAML frontmatter + markdown body. Frontmatter is validated with pydantic v2; **unknown keys are tolerated (`extra="allow"`)** so awesome-copilot files import with zero rework even as that repo evolves (risk R3).

### 4.1 Role — `content/agents/*.agent.md`

Maps 1:1 to awesome-copilot `agents/` (frontmatter: `name`, `description`, optional `model`, `tools`).

```yaml
---
name: Architect                          # display name (optional; slug = filename)
description: System design, ADRs, module boundaries. Use before non-trivial changes.
model: default                           # optional, passthrough
tools: [search, read]                    # optional, passthrough (client-specific)
tags: [design]                           # Agent HQ extension, optional
---
# Architect                              ← body = persona prompt (kept verbatim on import)
You are a principal architect…
```

```python
# schema/role.py (sketch)
class RoleFrontmatter(BaseModel):
    model_config = ConfigDict(extra="allow")  # tolerate unknown keys (R3)
    name: str | None = None
    description: str  # required for every kind
    model: str | None = None  # passthrough (client-specific)
    tools: list[str] | None = None
    tags: list[str] | None = None
```

### 4.2 Instruction — `content/instructions/*.instructions.md` (+ conventions)

Maps to awesome-copilot `instructions/` (`description`, `applyTo` glob(s)).

```yaml
---
description: Git hygiene — small commits, no secrets, never commit to main.
applyTo: '**'                            # string or array, as in awesome-copilot
tags: [process]                          # Agent HQ extension
---
## Rules
- …
```

### 4.3 Convention — `content/conventions/*.instructions.md` *(decision DD5)*

Conventions **are** instructions (identical schema) — same `applyTo`/`tags` semantics, different directory + conventionally a `stack` tag (`typescript`, `node`, `python`). The catalog serves them through the same `list_instructions` / `get_instruction` tools, tagged by directory. One schema instead of two; imports still trivial.

```yaml
---
description: TypeScript conventions — strict mode, no any, named exports…
applyTo: ['**/*.ts', '**/*.tsx']
tags: [typescript, convention]
---
```

### 4.4 Workflow — `content/workflows/*.workflow.md` *(original type)*

awesome-copilot's `workflows/` directory holds repo-ops reports, not dev processes — so this is Agent HQ's own type with a machine-readable phase structure (frontmatter) plus human-readable detail (body).

```yaml
---
name: Standard Feature
description: Phased feature development with quality gates.
version: "1"
phases:
  - id: discover
    title: Discovery & Context
    checklist:
      - "Map the relevant code area (use acquire-codebase-knowledge if unfamiliar)"
      - "State acceptance criteria; confirm with the user"
    gate: { kind: manual }                # user must approve before design
  - id: design
    title: Design
    checklist: ["Design notes in docs/design/<feature>.md"]
    gate: { kind: artifact, pattern: "docs/design/**" }
  - id: implement
    title: Implementation
    checklist: ["Code written", "Unit tests added and passing"]
    gate: { kind: checklist-complete }
  - id: review
    title: Review
    checklist: ["Self-review", "Security-relevant changes reviewed w/ security-reviewer role"]
    gate: { kind: manual }
  - id: ship
    title: Ship
    checklist: ["Tests green", "Docs/changelog updated", "PR description complete"]
    gate: { kind: artifact, pattern: "**" }   # = "exists": agent confirms via evidence
---
## Phase details            ← human-readable elaboration per phase
### discover
…
```

Gate kinds (v1): `none` · `manual` (requires `approved: true` in report) · `artifact` (glob exists under project) · `checklist-complete`.

### 4.5 Profile — `content/profiles/*.profile.yaml` *(original type, pure YAML)*

```yaml
id: node-web
name: Node.js Web Service (TypeScript)
description: TypeScript/Node API or web service projects.
matches:                               # used only when no pinned profile
  anyOf:
    - { file: "package.json" }
    - { file: "package.json", containsAny: ["express", "fastify", "next", "typescript"] }
stack: [typescript, node]
defaults:
  workflow: standard-feature
  roles: [architect, engineer, code-reviewer, test-engineer]
  instructions: [git-hygiene, agent-safety, ts-conventions, node-api]
  skills: [acquire-codebase-knowledge]
```

**Profile selection order (matcher):**
1. **Pinned** — project's `.agent-hq/profile.yaml` names a profile id → exact pick.
2. **Auto** — `catalog/detect.py` reads manifest signals from `projectPath` (package.json deps, pyproject.toml, go.mod, Cargo.toml, …) → each profile's `matches` rules score; highest score with ties broken by file order; no score → `default`.
3. **Fallback** — built-in `default` profile (generic instructions + standard workflow), guaranteed non-empty bundle.

### 4.6 Skill — `content/skills/<name>/SKILL.md`

Maps to awesome-copilot / Claude skill convention: `name`, `description`, optional `license`, `compatibility`, `metadata`, `argument-hint`. Slug = directory name. Sibling files (`scripts/`, `references/`) are listed in `get_skill` output as a path manifest (paths only — the server never executes skill scripts; the agent runs them with its own tools).

---

## 5. Tool Contracts

All tools: JSON input/output (pydantic-defined — FastMCP derives each tool's MCP JSON schema from the typed handler signature), snake_case names under the `agent_hq` prefix. Nine tools in v1 core, two added in phase 6.

| Tool | Input | Returns |
|------|-------|---------|
| `agent_hq.bootstrap` | `{ projectPath: string, hints?: Record<string,string> }` | `Bundle` (§5.1) |
| `agent_hq.content_info` | `{}` | `{ contentVersion, counts: {roles, instructions, skills, workflows, profiles}, profileIds }` |
| `agent_hq.list_roles` | `{ tag?: string }` | `RoleSummary[]` = `{slug, name, description}` |
| `agent_hq.get_role` | `{ slug }` | `{ slug, name, description, body (markdown) }` |
| `agent_hq.list_instructions` | `{ tag?: string, convention?: boolean }` | `InstructionSummary[]` = `{slug, description, applyTo?}` |
| `agent_hq.get_instruction` | `{ slug }` | `{ slug, description, body }` |
| `agent_hq.list_skills` | `{}` | `SkillSummary[]` = `{slug, description, files?}` |
| `agent_hq.get_skill` | `{ slug }` | `{ slug, description, body, files: string[] }` |
| `agent_hq.list_workflows` | `{}` | `WorkflowSummary[]` = `{slug, name, description, phases: {id,title}[]}` |
| `agent_hq.get_workflow` | `{ slug, phaseId? }` | full workflow (or single-phase view: checklist + gate + body section) |
| `agent_hq.get_checklist` | `{ workflowSlug, phaseId }` | `{ phase, checklist: string[], gate, nextAfterPass }` |
| `agent_hq.report_progress` *(P6)* | `{ projectPath?, workflowSlug, phaseId, completed: number[], evidence?: string, approved?: boolean }` | `{ ok, flags: Flag[], nextPhase? }` |
| `agent_hq.get_progress` *(P6)* | `{ projectPath?, workflowSlug? }` | board: per-phase status/timestamps/flags |

**Token-efficiency rule (G5):** `list_*` returns slugs + one-line descriptions only; full markdown travels via `get_*`. Exception: the bootstrap bundle carries **full instruction text** (small, needed immediately) but roles/skills as summaries only.

### 5.1 Bundle shape (`bootstrap` return)

```jsonc
{
  "contentVersion": "1a8ae39",            // digest → staleness detection
  "profile": { "id": "node-web", "source": "auto" },   // source: pinned|auto|fallback
  "workflow": {
    "slug": "standard-feature",
    "phases": [
      { "id": "discover", "title": "Discovery & Context",
        "checklist": ["Map the relevant code area…", "State acceptance criteria…"],
        "gate": { "kind": "manual" } }
      /* …all phases, checklists included (needed at session start) */
    ]
  },
  "instructions": [ { "slug": "git-hygiene", "description": "…", "body": "…" } ],
  "roles": [ { "slug": "architect", "name": "Architect", "description": "…" } ],
  "skills": [ { "slug": "acquire-codebase-knowledge", "description": "…" } ],
  "nextAction": "Start phase 'discover': complete its checklist, then call agent_hq.report_progress."
}
```

Expected size: ~2–4 k tokens for a typical bundle (measured in phase 3; hard cap + summarization fallback if a profile misbehaves — risk R4).

---

## 6. Design Decisions

| # | Decision | Rationale | Alternatives considered |
|---|----------|-----------|-------------------------|
| DD1 | **Python** (≥ 3.11, `uv` workspace) + official `mcp` SDK (FastMCP) + pydantic v2 | Owner decision (D1, 2026-09-24): maintainability for the project owner. Official Python SDK is mature; pydantic v2 doubles as content validator *and* tool-schema mechanism (FastMCP builds MCP schemas from typed handlers); one language for server *and* CLI; `uv` gives fast, reproducible envs + a committed lockfile | TypeScript (`@modelcontextprotocol/sdk` + zod) — technically equally viable; set aside in favor of owner maintainability |
| DD2 | **stdio** transport in v1 | Every target client supports stdio via a one-file `mcp.json`; zero infra for a single-user local server | Streamable-HTTP (v2) — `transport/http.ts` added later; tools are transport-agnostic by construction |
| DD3 | **Monorepo**: `server/` + `cli/` + `client/` + `content/` in one git repo | One clone, one version, content changes review alongside code; server takes `AGENT_HQ_CONTENT` path so content can be split into its own repo later with *zero code change* | Separate content repo — deferred; needs its own CI/publishing story |
| DD4 | **Follow awesome-copilot file conventions**; tolerate unknown frontmatter keys | Community content (800+ files) imports with zero rework; MIT license; conventions are stable & officially schema'd | Inventing our own format — would orphan the ecosystem |
| DD5 | **Conventions = instructions** (same schema, own directory + `stack` tag) | One schema, one tool surface; "convention" is a categorization, not a behavior difference | Separate `Convention` type — extra schema/tools for no capability gain |
| DD6 | **Pull-based bootstrap via AGENTS.md stub** | MCP cannot inject into system prompts; a two-paragraph stub is the reliable trigger across clients; bootstrap is idempotent and cheap | Relying on client-native "additional instructions" fields — client-specific, not portable |
| DD7 | **State = JSON files** in `~/.agent-hq/state/` (phase 6) | Single user, zero deps, human-inspectable, trivially testable; atomic writes (tmp+rename) | SQLite — v2 if multi-workflow scale demands |
| DD8 | **≤ 300 lines per source file**, enforced by CI `check:lines` (docs exempt) | User rule; keeps modules swappable & reviewable; per-file budgets in §2.2 make violations visible early | None — this is a fixed requirement |
| DD9 | **Progressive disclosure** for token efficiency | Bundles stay ~2–4 k tokens; full content on demand | Dump everything at bootstrap — burns context window every session |
| DD10 | **Pin `mcp` SDK version; isolate SDK surface** to `transport/stdio.py` + `tools/registry.py` | The Python SDK's API has churned across releases (FastMCP method renames); isolation bounds the blast radius of version bumps | — |

---

## 7. Risks & Mitigations

| # | Risk | Likelihood | Mitigation |
|---|------|-----------|------------|
| R1 | Clients differ in how reliably they obey tool outputs (some agents "forget" the workflow) | High | AGENTS.md stub wording tuned per client in phase 4; gates + flags make drift *visible*; real-client smoke tests per D4 |
| R2 | stdio server CWD ≠ project dir (client spawn quirks) | Medium | `projectPath` is an **explicit required parameter** of bootstrap — no CWD inference anywhere in the critical path |
| R3 | awesome-copilot frontmatter drift (they add keys/fields over time) | Medium | pydantic `extra="allow"`; fixture tests pin snapshots from a dated revision; failures degrade to "tolerated warning", never crash |
| R4 | Token bloat: a profile references too much content → bundle explodes | Low-Med | Bundle size budget + measured in phase 3; oversized instructions return summary + `get_*` pointer instead of body |
| R5 | State staleness (agent works for hours without reporting) | Medium | `get_progress` shows last-activity timestamps; stub instructs report-per-phase; v2: heartbeat tool |
| R6 | 300-line discipline erodes over time | Medium | CI `check:lines` (hard fail) + per-file budgets documented in §2.2 |
| R7 | MCP SDK breaking changes on upgrade | Medium | Pinned dep; adapter isolation (DD10); e2e JSON-RPC smoke in CI catches protocol-level regressions |
| R8 | Content quality: imported community content is noisy/inconsistent | Medium | Curation pass in phase 5 (trim to what we trust); `agent-hq validate` as PR gate; community additions are opt-in via `import` |

---

## 8. Testing & Performance Notes

- **Fixtures:** real awesome-copilot files (agents/instructions/skills) captured at implementation time into `server/test/fixtures/` — compatibility is proven against the actual ecosystem, not synthetic data.
- **Stack-matching tests** use minimal fake trees (`package.json` with different dep sets, `pyproject.toml`, …) — no network.
- **E2E (CI):** spawn the server (`uv run agent-hq-server`) on stdio, speak raw JSON-RPC: `initialize` → `tools/list` → `bootstrap(fixtureProject)` → `get_checklist` → `report_progress` sequence. This is the regression backbone; runs in seconds.
- **Performance targets:** catalog load < 100 ms for 500 content files; any tool call < 50 ms (local disk, in-memory index); bundle assembly O(profile refs), not O(content tree).
