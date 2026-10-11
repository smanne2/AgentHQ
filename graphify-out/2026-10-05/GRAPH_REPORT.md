# Graph Report - special-telegram  (2026-10-05)

## Corpus Check
- 62 files · ~29,633 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .toml 1, .lock 1)

## Summary
- 687 nodes · 1177 edges · 45 communities (36 shown, 9 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `908b5ad7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ContentBase
- schema/__init__.py
- test_util.py
- registry.py
- pathlib
- 5. Detailed Implementation Plan (phases → tasks → acceptance)
- matcher.py
- Accessibility Expert
- Document Sections
- test_mcp_stdio.py
- Agent HQ — Technical Design
- test_scaffold.py
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
- copilot-instructions.md
- agent-hq
- agent-hq-workspace
- Catalog
- pick_profile
- load
- catalog.py
- detect.py
- Framework-Specific: Vue (VU1-VU3)
- _flatten

## God Nodes (most connected - your core abstractions)
1. `Catalog` - 36 edges
2. `load()` - 26 edges
3. `ErrorView` - 22 edges
4. `create_server()` - 18 edges
5. `Accessibility Expert` - 17 edges
6. `pick_profile()` - 16 edges
7. `_dump()` - 16 edges
8. `catalog()` - 16 edges
9. `Accessibility Standards` - 16 edges
10. `Development Standards` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Change Log` --references--> `test_mcp_stdio_invalid_tool_is_tool_error()`  [INFERRED]
  documents/initial-plan/tracking.md → server/tests/test_mcp_stdio.py
- `agent-hq` --depends_on--> `agent-hq-server`  [EXTRACTED]
  cli/pyproject.toml → server/pyproject.toml
- `assemble_bundle()` --uses--> `ProfileItem`  [INFERRED]
  server/src/agent_hq_server/catalog/bundle.py → server/src/agent_hq_server/catalog/catalog.py
- `_get_skill_files()` --uses--> `Skill`  [INFERRED]
  server/src/agent_hq_server/catalog/bundle.py → server/src/agent_hq_server/catalog/catalog.py
- `_role_summary()` --uses--> `Role`  [INFERRED]
  server/src/agent_hq_server/tools/bootstrap.py → server/src/agent_hq_server/catalog/catalog.py

## Import Cycles
- None detected.

## Communities (45 total, 9 thin omitted)

### Community 0 - "ContentBase"
Cohesion: 0.10
Nodes (6): ContentBase, InstructionFrontmatter, RoleFrontmatter, SkillFrontmatter, Phase, WorkflowFrontmatter

### Community 1 - "schema/__init__.py"
Cohesion: 0.09
Nodes (23): InstructionSummary, ChecklistView, ContentInfoView, Counts, ErrorView, InstructionViewFull, RoleView, SkillView (+15 more)

### Community 2 - "test_util.py"
Cohesion: 0.12
Nodes (10): content_digest(), slug_from_dir(), slug_from_filename(), _slugify(), test_digest_changes_with_content(), test_digest_missing_dir(), test_slug_from_dir_uses_skill_directory(), test_slug_from_filename_explicit_suffix() (+2 more)

### Community 3 - "registry.py"
Cohesion: 0.07
Nodes (12): main(), _repo_root(), build(), Config, default_content_path(), default_project_path(), _expand(), resolve_project_path() (+4 more)

### Community 4 - "pathlib"
Cohesion: 0.06
Nodes (23): parse_markdown(), parse_yaml_file(), ParsedDoc, _strip(), read_pin_file(), ContentError, Issue, Result (+15 more)

### Community 5 - "5. Detailed Implementation Plan (phases → tasks → acceptance)"
Cohesion: 0.05
Nodes (35): 1. Overview, 2. Goals / Non-Goals, 3. How Consistency Works (Bootstrap Handshake), 4. Architecture, 5. Detailed Implementation Plan (phases → tasks → acceptance), 6. Validation Strategy (summary), 7. Decisions (all resolved 2026-09-24), 8. v2 Ideas (parked, not planned) (+27 more)

### Community 6 - "matcher.py"
Cohesion: 0.15
Nodes (7): BundleMatchInput, _rule_matches(), _score(), Defaults, FileMatch, Matches, Profile

### Community 7 - "Accessibility Expert"
Cohesion: 0.06
Nodes (35): Accessibility Expert, Advanced Capabilities You Know, Angular, Anti-Patterns to Avoid, Best Practices Summary, Checklists, CI Example (GitHub Actions), Common Scenarios You Excel At (+27 more)

### Community 8 - "Document Sections"
Cohesion: 0.08
Nodes (25): 1. Gather Required Information, 2. Determine ADR Number, 3. Generate ADR Document in Markdown, ADR Generator Agent, Agent Success Criteria, [Alternative Name], Alternatives Considered, Consequences (+17 more)

### Community 9 - "test_mcp_stdio.py"
Cohesion: 0.13
Nodes (7): _call(), _Client, _now(), project_dir(), _spawn(), test_mcp_stdio_full_roundtrip(), test_mcp_stdio_invalid_tool_is_tool_error()

### Community 10 - "Agent HQ — Technical Design"
Cohesion: 0.09
Nodes (23): 1.1 The problem, 1.2 What Agent HQ adds, 1. Problem & Value, 2.1 Components & dependency rules, 2.2 Repository layout (monorepo, decision D3 · Python per D1), 2. Architecture, 3.1 Bootstrap handshake (session start), 3.2 On-demand retrieval (during work) (+15 more)

### Community 12 - "create_server"
Cohesion: 0.22
Nodes (14): create_server(), bootstrap(), content_info(), get_checklist(), get_instruction(), get_role(), get_skill(), get_workflow() (+6 more)

### Community 13 - "Development Standards"
Cohesion: 0.11
Nodes (18): Actions, API Routes and SSR, Architecture, Astro Development Instructions, Client-Side Interactivity, Component Design, Content Collections, Data Fetching (+10 more)

### Community 14 - "Accessibility Standards"
Cohesion: 0.22
Nodes (8): Accessibility Standards, Color Contrast Quick Reference, Five Rules of ARIA, Keyboard Interaction Reference, Legal Enforcement Context (2026), Non-Text Contrast (WCAG 1.4.11 AA), Text Contrast (WCAG 1.4.3 AA), Widget-Specific Patterns

### Community 15 - "Acquire Codebase Knowledge"
Cohesion: 0.15
Nodes (12): Acquire Codebase Knowledge, Anti-Patterns, Bundled Assets, Enhanced Scan Output Sections, Focus Area Mode, Gotchas, Output Contract (Required), Phase 1: Scan and Read Intent (+4 more)

### Community 16 - "Agent Safety & Governance"
Cohesion: 0.20
Nodes (9): Agent Safety & Governance, Audit & Observability, Code Patterns, Common Mistakes, Content Safety, Core Principles, Framework-Specific Notes, Multi-Agent Safety (+1 more)

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
Cohesion: 0.25
Nodes (7): 0. At the start of every session: read `context.txt`, 1. Plan before code — planning docs live in `documents/`, 2. Explicit approval gates implementation, 3. Use the Graphify skill for architecture and relationship questions, 4. Update the tracking document — automatically, immediately, AGENTS.md — working rules for AI agents in this repo, Repo invariants (from the approved plan)

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

### Community 38 - "Catalog"
Cohesion: 0.09
Nodes (27): assemble_bundle(), _get_skill_files(), _resolve_instructions(), _resolve_roles(), _resolve_skills(), _resolve_workflow(), Catalog, Bundle (+19 more)

### Community 39 - "pick_profile"
Cohesion: 0.17
Nodes (12): _any_glob_matches(), match_instructions(), pick_profile(), test_auto_match_on_file_presence(), test_auto_match_on_manifest_signals(), test_instruction_matching_by_globs(), test_no_profiles_raises(), test_no_signals_fall_back_to_default() (+4 more)

### Community 40 - "load"
Cohesion: 0.21
Nodes (10): load(), test_astro_comma_globs_normalized(), test_counts_helper(), test_digest_stable_and_sensitive(), test_duplicate_slug_across_directories_flagged(), test_fixture_tree_loads_fast(), test_fixture_tree_loads_with_zero_rework(), test_malformed_file_becomes_issue_not_crash() (+2 more)

### Community 41 - "catalog.py"
Cohesion: 0.33
Nodes (8): _append(), _build_item(), Instruction, _kind_for(), ProfileItem, Role, Skill, Workflow

### Community 43 - "Framework-Specific: Vue (VU1-VU3)"
Cohesion: 0.50
Nodes (4): Framework-Specific: Vue (VU1-VU3), VU1: `@click` on Non-Interactive Element Without Role and Keyboard, VU2: `v-if` Toggle Without Focus Management, VU3: `v-html` Injecting Content Without Accessible Structure

## Knowledge Gaps
- **216 isolated node(s):** `agent-hq`, `agent-hq-workspace`, `agent-hq-server`, `graphify`, `0. At the start of every session: read `context.txt`` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 381 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_mcp_stdio_invalid_tool_is_tool_error()` connect `test_mcp_stdio.py` to `5. Detailed Implementation Plan (phases → tasks → acceptance)`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `Catalog` (e.g. with `assemble_bundle()` and `_resolve_instructions()`) actually correct?**
  _`Catalog` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `agent-hq`, `agent-hq-workspace`, `agent-hq-server` to the rest of the system?**
  _216 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ContentBase` be split into smaller, more focused modules?**
  _Cohesion score 0.0960591133004926 - nodes in this community are weakly interconnected._
- **Why does `Change Log` connect `5. Detailed Implementation Plan (phases → tasks → acceptance)` to `test_mcp_stdio.py`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Should `schema/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08758503401360544 - nodes in this community are weakly interconnected._
- **Should `test_util.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12318840579710146 - nodes in this community are weakly interconnected._