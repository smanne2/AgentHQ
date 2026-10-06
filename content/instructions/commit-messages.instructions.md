---
description: Commit message conventions — imperative subject, wrap at 72, body explains why.
tags: [process, git]
---
# Commit Messages

- **Subject**: imperative mood, ≤ 72 chars, no trailing period.
  `add retry to webhook client`, not `added`, not `fixing stuff`.
- **Scope (optional)**: prefix with the area when it helps — `api: add …`, `test: …`.
- **Body**: explain *why* the change was made and any trade-off, wrapped at 72.
  Omit the body when the subject is self-explanatory.
- **Reference**: link the issue/PR (`Fixes #123`) when applicable.
- **Conventional Commits** are welcome but not required; consistency over ceremony.
- One logical change per commit (see git-hygiene).
