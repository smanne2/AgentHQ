---
name: adr-writer
description: 'Write a concise Architecture Decision Record when a real trade-off was made. Trigger for "write an ADR", "document this decision", or when the Architect role recommends one.'
argument-hint: 'Optional: the decision title or a link to the design notes'
---
# ADR Writer

Write a short, permanent record of a significant decision so future readers
understand *why*, not just *what*.

## When to write one
- A real trade-off was made between viable alternatives.
- The decision is hard to reverse, or its rationale is non-obvious.
- Not for: routine implementation choices, style, or reversible details.

## Template (keep it under ~1 page)
```
# ADR-<n>: <decision title>
- Status: proposed | accepted | superseded-by-ADR-<m>
- Date: <YYYY-MM-DD>

## Context
What is the problem and what constraints/needs force a decision?

## Decision
The decision, stated in one or two sentences.

## Consequences
Positive, negative, and neutral results we accept; what to watch for.

## Alternatives considered
Each alternative and the reason it was rejected.
```

## Rules
- Number sequentially in `docs/adr/` (e.g. `docs/adr/0001-<slug>.md`).
- Write in the present tense; ADRs are immutable — to change, supersede.
- Every claim should be grounded in the code or constraints that drove it.
