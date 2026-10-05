# Graph Report - special-telegram  (2026-09-26)

## Corpus Check
- 60 files · ~28,076 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .toml 1, .lock 1)

## Summary
- 662 nodes · 1081 edges · 38 communities (33 shown, 5 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 48 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `21d2665d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- schema/__init__.py
- Catalog
- catalog.py
- registry.py
- test_frontmatter.py
- 5. Detailed Implementation Plan (phases → tasks → acceptance)
- matcher.py
- Accessibility Expert
- Document Sections
- test_mcp_stdio.py
- Agent HQ — Technical Design
- test_schemas.py
- create_server
- Development Standards
- Accessibility Standards
- Acquire Codebase Knowledge
- Agent Safety & Governance
- main.py
- ARIA Anti-Patterns (A1-A8)
- Semantic HTML Anti-Patterns (S1-S8)
- After Fixing a comment
- Keyboard and Focus Anti-Patterns (K1-K7)
- AGENTS.md — working rules for AI agents in this repo
- Form Anti-Patterns (F1-F6)
- AI Agent Architecture
- Phase details
- Visual and Color Anti-Patterns (V1-V5)
- Accessibility Checklist (POUR)
- Media Anti-Patterns (D1-D4)
- Framework-Specific: Angular (NG1-NG4)
- Framework-Specific: React / Next.js (RX1-RX4)
- WCAG 2.2 Quick Reference (AA Level)
- Agent HQ
- agent_hq_cli/__init__.py
- copilot-instructions.md
- agent-hq
- util/__init__.py
- agent-hq-workspace

## God Nodes (most connected - your core abstractions)
1. `Catalog` - 29 edges
2. `load()` - 25 edges
3. `ErrorView` - 20 edges
4. `create_server()` - 18 edges
5. `Accessibility Expert` - 17 edges
6. `_dump()` - 16 edges
7. `Accessibility Standards` - 16 edges
8. `Development Standards` - 16 edges
9. `pick_profile()` - 15 edges
10. `catalog()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `agent-hq` --depends_on--> `agent-hq-server`  [EXTRACTED]
  cli/pyproject.toml → server/pyproject.toml
- `_role_summary()` --uses--> `Role`  [INFERRED]
  server/src/agent_hq_server/tools/bootstrap.py → server/src/agent_hq_server/catalog/catalog.py
- `get_role()` --uses--> `Role`  [INFERRED]
  server/src/agent_hq_server/tools/roles.py → server/src/agent_hq_server/catalog/catalog.py
- `match_instructions()` --uses--> `Instruction`  [INFERRED]
  server/src/agent_hq_server/catalog/matcher.py → server/src/agent_hq_server/catalog/catalog.py
- `_resolve_instructions()` --uses--> `Instruction`  [INFERRED]
  server/src/agent_hq_server/tools/bootstrap.py → server/src/agent_hq_server/catalog/catalog.py

## Import Cycles
- None detected.

## Communities (38 total, 5 thin omitted)

### Community 0 - "schema/__init__.py"
Cohesion: 0.07
Nodes (47): model_validator, pydantic, Path, Return ``(pinned_profile_id, warning)`` for the given project directory.…, read_pin_file(), Bundle, BundleProfile, InstructionSummary (+39 more)

### Community 1 - "Catalog"
Cohesion: 0.07
Nodes (52): Catalog, ChecklistView, ContentInfoView, Counts, ErrorView, InstructionViewFull, BaseModel, On-demand tool return views (technical.md §5 ``get_*`` + list rows). These are… (+44 more)

### Community 2 - "catalog.py"
Cohesion: 0.07
Nodes (50): hashlib, Kind, _append(), _build_item(), _flatten(), Instruction, _kind_for(), load() (+42 more)

### Community 3 - "registry.py"
Cohesion: 0.07
Nodes (35): argparse, logging, mcp_server_fastmcp, Namespace, main(), Path, Fail if any source file exceeds the 300-line budget (plan rule G6). Documents…, _repo_root() (+27 more)

### Community 4 - "test_frontmatter.py"
Cohesion: 0.08
Nodes (36): collections_abc, dataclasses, os, pathlib, parse_markdown(), parse_yaml_file(), ParsedDoc, Path (+28 more)

### Community 5 - "5. Detailed Implementation Plan (phases → tasks → acceptance)"
Cohesion: 0.05
Nodes (35): 1. Overview, 2. Goals / Non-Goals, 3. How Consistency Works (Bootstrap Handshake), 4. Architecture, 5. Detailed Implementation Plan (phases → tasks → acceptance), 6. Validation Strategy (summary), 7. Decisions (all resolved 2026-09-24), 8. v2 Ideas (parked, not planned) (+27 more)

### Community 6 - "matcher.py"
Cohesion: 0.08
Nodes (34): pathspec, ProfileSource, re, _any_glob_matches(), BundleMatchInput, match_instructions(), pick_profile(), BaseModel (+26 more)

### Community 7 - "Accessibility Expert"
Cohesion: 0.06
Nodes (35): Accessibility Expert, Advanced Capabilities You Know, Angular, Anti-Patterns to Avoid, Best Practices Summary, Checklists, CI Example (GitHub Actions), Common Scenarios You Excel At (+27 more)

### Community 8 - "Document Sections"
Cohesion: 0.08
Nodes (25): 1. Gather Required Information, 2. Determine ADR Number, 3. Generate ADR Document in Markdown, ADR Generator Agent, Agent Success Criteria, [Alternative Name], Alternatives Considered, Consequences (+17 more)

### Community 9 - "test_mcp_stdio.py"
Cohesion: 0.14
Nodes (17): json, Popen, queue, _call(), _Client, _now(), project_dir(), fixture (+9 more)

### Community 10 - "Agent HQ — Technical Design"
Cohesion: 0.09
Nodes (23): 1.1 The problem, 1.2 What Agent HQ adds, 1. Problem & Value, 2.1 Components & dependency rules, 2.2 Repository layout (monorepo, decision D3 · Python per D1), 2. Architecture, 3.1 Bootstrap handshake (session start), 3.2 On-demand retrieval (during work) (+15 more)

### Community 11 - "test_schemas.py"
Cohesion: 0.09
Nodes (7): CaptureFixture, pytest, Agent HQ MCP server — typed content service for agent guidance., Phase 0 smoke tests: workspace wiring, imports, console entry points., Entry point parses flags and exits cleanly (stdio mode is covered in…, test_server_main_version(), Pydantic content schemas: required fields, normalization, tolerance.

### Community 12 - "create_server"
Cohesion: 0.22
Nodes (19): FastMCP, create_server(), bootstrap(), content_info(), get_checklist(), get_instruction(), get_role(), get_skill() (+11 more)

### Community 13 - "Development Standards"
Cohesion: 0.11
Nodes (18): Actions, API Routes and SSR, Architecture, Astro Development Instructions, Client-Side Interactivity, Component Design, Content Collections, Data Fetching (+10 more)

### Community 14 - "Accessibility Standards"
Cohesion: 0.15
Nodes (12): Accessibility Standards, Color Contrast Quick Reference, Five Rules of ARIA, Framework-Specific: Vue (VU1-VU3), Keyboard Interaction Reference, Legal Enforcement Context (2026), Non-Text Contrast (WCAG 1.4.11 AA), Text Contrast (WCAG 1.4.3 AA) (+4 more)

### Community 15 - "Acquire Codebase Knowledge"
Cohesion: 0.15
Nodes (12): Acquire Codebase Knowledge, Anti-Patterns, Bundled Assets, Enhanced Scan Output Sections, Focus Area Mode, Gotchas, Output Contract (Required), Phase 1: Scan and Read Intent (+4 more)

### Community 16 - "Agent Safety & Governance"
Cohesion: 0.20
Nodes (9): Agent Safety & Governance, Audit & Observability, Code Patterns, Common Mistakes, Content Safety, Core Principles, Framework-Specific Notes, Multi-Agent Safety (+1 more)

### Community 17 - "main.py"
Cohesion: 0.22
Nodes (8): callback, Agent HQ CLI entry point. Full commands (`init`, `doctor`, `validate`,…, Keep the app multi-command so `agent-hq version` works in Phase 0., Print the Agent HQ CLI version., _root(), version(), command, typer

### Community 18 - "ARIA Anti-Patterns (A1-A8)"
Cohesion: 0.22
Nodes (9): A1: Redundant ARIA on Native Elements, A2: `aria-hidden="true"` on Focusable Element, A3: Missing Required ARIA Properties, A4: Invalid ARIA Role Values, A5: ARIA Where Native HTML Works, A6: Missing `aria-label` on Icon-Only Buttons, A7: `role="presentation"` on Focusable Elements, A8: Missing Live Region for Dynamic Content (+1 more)

### Community 19 - "Semantic HTML Anti-Patterns (S1-S8)"
Cohesion: 0.22
Nodes (9): S1: Missing `lang` Attribute on `<html>`, S2: Multiple `<h1>` Per Page, S3: Heading Level Gaps, S4: Div Soup — No Landmark Elements, S5: Layout Tables Without `role="presentation"`, S6: Data Tables Without Headers, S7: Non-Descriptive Link Text, S8: Interactive Elements Without Semantic HTML (+1 more)

### Community 20 - "After Fixing a comment"
Cohesion: 0.25
Nodes (7): Addressing Comments, After Fixing a comment, Commit the changes, Fix next comment, Run tests, Universal PR Comment Addresser, When to address or not address comments

### Community 21 - "Keyboard and Focus Anti-Patterns (K1-K7)"
Cohesion: 0.25
Nodes (8): K1: `onClick` Without `onKeyDown` on Non-Native Elements, K2: Positive `tabindex` Values, K3: Focus Trap Without Escape, K4: Missing Skip Link, K5: `outline: none` Without Replacement, K6: Mouse-Only Interactions, K7: Focus Not Returned After Custom Modal Close, Keyboard and Focus Anti-Patterns (K1-K7)

### Community 22 - "AGENTS.md — working rules for AI agents in this repo"
Cohesion: 0.29
Nodes (6): 0. At the start of every session: read `context.txt`, 1. Plan before code — planning docs live in `documents/`, 2. Explicit approval gates implementation, 3. Update the tracking document — automatically, immediately, AGENTS.md — working rules for AI agents in this repo, Repo invariants (from the approved plan)

### Community 23 - "Form Anti-Patterns (F1-F6)"
Cohesion: 0.29
Nodes (7): F1: Input Without Associated Label, F2: Error Messages Not Linked to Input, F3: Required Field Indicated Only by Color or `*`, F4: No Error Summary or Focus on First Error, F5: CAPTCHA Without Accessible Alternative, F6: Placeholder as Label, Form Anti-Patterns (F1-F6)

### Community 24 - "AI Agent Architecture"
Cohesion: 0.29
Nodes (6): AI Agent Architecture, Choose a route, Final artifacts, How to work, Package metadata, Shared decision rules

### Community 25 - "Phase details"
Cohesion: 0.29
Nodes (6): design, discover, implement, Phase details, review, ship

### Community 26 - "Visual and Color Anti-Patterns (V1-V5)"
Cohesion: 0.33
Nodes (6): V1: Insufficient Text Contrast, V2: Information Conveyed by Color Alone, V3: Fixed Font Sizes Preventing Resize, V4: Content Not Reflowing at 320px, V5: Animation Without `prefers-reduced-motion`, Visual and Color Anti-Patterns (V1-V5)

### Community 27 - "Accessibility Checklist (POUR)"
Cohesion: 0.40
Nodes (5): Accessibility Checklist (POUR), Operable, Perceivable, Robust, Understandable

### Community 28 - "Media Anti-Patterns (D1-D4)"
Cohesion: 0.40
Nodes (5): D1: Informational Image Without Alt Text, D2: Decorative Image with Non-Empty Alt, D3: Video Without Captions, D4: Audio/Video Autoplay, Media Anti-Patterns (D1-D4)

### Community 29 - "Framework-Specific: Angular (NG1-NG4)"
Cohesion: 0.40
Nodes (5): Framework-Specific: Angular (NG1-NG4), NG1: `(click)` on `<div>` Without Role and Keyboard Support, NG2: Missing `cdkTrapFocus` in Modal Components, NG3: Route Change Without LiveAnnouncer, NG4: Template-Driven Forms Without Accessible Validation

### Community 30 - "Framework-Specific: React / Next.js (RX1-RX4)"
Cohesion: 0.40
Nodes (5): Framework-Specific: React / Next.js (RX1-RX4), RX1: Missing `htmlFor` on `<label>`, RX2: SPA Route Change Without Focus Management, RX3: Fragment Root Causing Focus Loss on Re-render, RX4: Injected HTML Without ARIA Consideration

### Community 31 - "WCAG 2.2 Quick Reference (AA Level)"
Cohesion: 0.40
Nodes (5): Operable, Perceivable, Robust, Understandable, WCAG 2.2 Quick Reference (AA Level)

### Community 32 - "Agent HQ"
Cohesion: 0.50
Nodes (3): Agent HQ, Development, Status

## Knowledge Gaps
- **216 isolated node(s):** `agent-hq`, `agent-hq-workspace`, `agent-hq-server`, `graphify`, `0. At the start of every session: read `context.txt`` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 379 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load()` connect `catalog.py` to `Catalog`, `registry.py`, `test_frontmatter.py`, `matcher.py`, `create_server`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Catalog` connect `Catalog` to `schema/__init__.py`, `catalog.py`, `test_frontmatter.py`, `matcher.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `create_server()` connect `create_server` to `catalog.py`, `registry.py`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `Catalog` (e.g. with `Issue` and `pick_profile()`) actually correct?**
  _`Catalog` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `agent-hq`, `agent-hq-workspace`, `agent-hq-server` to the rest of the system?**
  _216 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `schema/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06830601092896176 - nodes in this community are weakly interconnected._
- **Should `Catalog` be split into smaller, more focused modules?**
  _Cohesion score 0.06954997077732321 - nodes in this community are weakly interconnected._