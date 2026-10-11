---
name: Standard Feature
description: Phased feature development with quality gates — the default workflow for new functionality.
version: "1"
phases:
  - id: discover
    title: Discovery & Context
    checklist:
      - "Map the relevant code area (use acquire-codebase-knowledge if unfamiliar)"
      - "State acceptance criteria; confirm with the user"
    gate:
      kind: manual
  - id: design
    title: Design
    checklist:
      - "Write design notes in docs/design/<feature>.md"
      - "Identify affected modules and risk areas"
    gate:
      kind: artifact
      pattern: docs/design/**
  - id: implement
    title: Implementation
    checklist:
      - "Code written"
      - "Unit tests added and passing"
    gate:
      kind: checklist-complete
  - id: review
    title: Review
    checklist:
      - "Self-review the diff"
      - "Security-relevant changes reviewed with a security reviewer role"
    gate:
      kind: manual
  - id: ship
    title: Ship
    checklist:
      - "All tests green"
      - "Docs and changelog updated"
    gate:
      kind: none
---

## Phase details

### discover
Establish context before writing any code. Confirm the acceptance criteria with
the user — everything after this phase is gated on that agreement.

### design
Small features may need a paragraph; anything touching more than one module
needs a written design note so the review phase has something concrete.

### implement
Write the change with tests in the same pass. No "tests later" — a checklist
item is only complete when the tests actually run and pass.

### review
Self-review, then apply the security-reviewer role to anything touching
auth, input handling, or secrets.

### ship
Green tests plus updated docs are the definition of done.
