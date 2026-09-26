# Agent HQ

A centralized MCP server that acts as the single source of truth for how coding agents behave: **roles**, **instructions**, **skills**, standardized **workflows**, and stack **conventions** — served to any MCP client (VS Code Copilot, Cline, Claude Desktop, …).

Every new project starts from the same guidance and process. Development stops being vague.

## Status

- Plan & design: [`documents/initial-plan/`](documents/initial-plan/) (approved 2026-09-24)
- Implementation: Phase 0–1 (scaffold + content core) in progress

## Development

Requires [uv](https://docs.astral.sh/uv/) and Python ≥ 3.11.

```sh
uv sync                 # install workspace (server + cli)
uv run pytest           # tests
uv run ruff check .     # lint
uv run python server/scripts/check_lines.py   # 300-line budget guard
```

Layout: `server/` (MCP server), `cli/` (`agent-hq` CLI), `content/` (git-versioned guidance content), `client/` (per-project templates).
