---
name: Refactor
description: Improve structure without changing behavior — baseline first, small verifiable steps.
version: "1"
phases:
  - id: scope
    title: Scope the Refactor
    checklist:
      - "Name the code to change and the goal (clarity, duplication, performance)"
      - "Define the non-goals — what stays the same"
    gate:
      kind: manual
  - id: baseline
    title: Behavior Baseline
    checklist:
      - "Existing tests identified and green"
      - "Characterization test added for behavior that has no test"
    gate:
      kind: checklist-complete
  - id: refactor
    title: Refactor
    checklist:
      - "Small, verifiable change applied"
      - "Baseline re-run green after each step"
    gate:
      kind: checklist-complete
  - id: review
    title: Review
    checklist:
      - "Diff reviewed: no behavior change, no mixed concerns"
      - "Linter/formatter clean"
    gate:
      kind: manual
  - id: ship
    title: Ship
    checklist:
      - "Full suite green"
      - "Diff summarized for the reviewer"
    gate:
      kind: none
---
## Phase details

### scope
A refactor without a goal is just churn. Name what improves and what must *not*
change, so the diff stays reviewable.

### baseline
You can't prove "no behavior change" without a baseline. Add a characterization
test where coverage is missing *before* touching the code.

### refactor
One small step at a time, each verified against the baseline. If an "improvement"
changes behavior, stop — that's a different task.

### review
Confirm the diff is a no-op behaviorally and mixes no concerns. Green baseline +
clean lint is the exit.

### ship
Suite green, diff summarized. Done.
