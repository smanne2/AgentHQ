---
description: Git hygiene — small focused commits, no secrets, never commit directly to the main branch.
tags: [process, git]
---
# Git Hygiene

- **Small, focused commits** — one logical change per commit; the message states
  *what* and *why*, not just what.
- **Never commit secrets** — no API keys, tokens, or passwords. Use the project's
  `.env.example` / secret store pattern.
- **Never commit directly to the main/default branch** — branch, open a PR, review.
- Keep the working tree clean; don't stage unrelated files or editor cruft.
- Add or update `gitignore` for new artifact types (build output, venvs, logs).
- Rebase/merge so history is linear and bisect-friendly when feasible.
