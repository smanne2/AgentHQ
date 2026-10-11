# Agent HQ

A centralized MCP server that acts as the single source of truth for how coding agents behave: **roles**, **instructions**, **skills**, standardized **workflows**, and stack **conventions** — served to any MCP client (VS Code Copilot, Cline, Claude Desktop, …).

Every new project starts from the same guidance and process. Development stops being vague.

## Quickstart (< 10 min)

### 1. Installation & Deployment (Docker)
The recommended way to run Agent HQ is via Docker for stability and isolation:
```bash
docker compose up -d
```
This starts the server in production mode on port 3000.

### 2. Configuration
Add Agent HQ to your MCP client (e.g., VS Code, Claude Desktop). Use the following SSE configuration:
- **Type**: `sse`
- **URL**: `http://localhost:3000/mcp`

Example for `mcp.json`:
```json
"agent-hq": {
  "type": "sse",
  "url": "http://localhost:3000/mcp"
}
```

### 3. Using Agent HQ in a Project
To start a governed session in your project:
1. Create an `.agent-hq/profile.yaml` in your project root (optional, otherwise it auto-detects).
2. The agent should first call `agent_hq.bootstrap({"projectPath": "./"})`.
3. Follow the returned workflow: one phase at a time, completing the checklist, and calling `agent_hq.report_progress` to pass the quality gates.

## Status

- Plan & design: [`documents/initial-plan/`](documents/initial-plan/) (approved 2026-09-24)
- Implementation: **Phase 0–6 complete** (core, MCP server, profiles, CLI, seed content, and state enforcement).

## Development

Requires [uv](https://docs.astral.sh/uv/) and Python ≥ 3.11.

```sh
uv sync --all-packages         # install workspace (server + cli)
uv run pytest                 # tests
uv run ruff check .           # lint
uv run python server/scripts/check_lines.py   # 300-line budget guard
```

Layout: `server/` (MCP server), `cli/` (`agent-hq` CLI), `content/` (git-versioned guidance content), `client/` (per-project templates).
