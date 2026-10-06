---
description: Safety rails for building governed AI-agent systems — fail closed, least privilege, audit everything.
tags: [process, safety]
---
# Agent Safety & Governance

Apply when writing code that uses agent frameworks, tool-calling LLMs, or
multi-agent orchestration.

## Core principles
- **Fail closed** — if a governance check errors or is ambiguous, deny the action.
- **Least privilege** — give agents the minimum tools/access needed for the task.
- **Append-only audit** — never modify or delete audit entries; immutability enables review.
- **Policy as config** — encode rules in YAML/JSON, not hardcoded.

## Tool access
- Maintain an explicit allowlist of tools; never give unrestricted access.
- Separate tool *registration* from tool *authorization*.
- Blocklist known-dangerous operations (shell, file deletion, DDL); require
  human-in-the-loop approval for high-impact actions (deploy, delete, send).
- Rate-limit tool calls to prevent runaway loops.

## Content & input safety
- Scan user input and tool arguments for prompt injection and secrets.
- Regex/list filters live in config so they update without code changes.
- Never log raw user content — log decisions and metadata only.

## Multi-agent
- When agents delegate, apply the most restrictive policy of either side.
- An inner agent never gets broader permissions than its caller.
