---
description: Code style (generic) — match the neighbors, keep it simple, avoid dead code.
tags: [style]
---
# Code Style (Generic)

- **Match the existing style** — naming, formatting, and structure of the files
  you're editing. When in doubt, copy the pattern of the nearest neighbor.
- **Keep it simple** — the smallest code that does the job; avoid premature
  abstraction and cleverness that outpaces readability.
- **No dead code** — remove unused functions, imports, and commented-out blocks.
- **Name things for intent** — a reader should infer purpose without reading on.
- **Extract the smallest meaningful unit** — a function that does one thing well.
- **Handle errors explicitly** at the boundary that owns them; don't swallow silently.
- Run the project's linter/formatter before finishing so the diff is clean.
