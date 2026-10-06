---
name: Bugfix
description: Find the root cause, fix it with a regression test, and verify. Use for reported defects.
version: "1"
phases:
  - id: reproduce
    title: Reproduce & Scope
    checklist:
      - "Reproduce the defect (command/steps recorded in the report)"
      - "State the expected vs. observed behavior; confirm with the user"
    gate:
      kind: manual
  - id: diagnose
    title: Root-Cause Analysis
    checklist:
      - "Identify the root cause with file/function references"
      - "Rule out or confirm the suspected cause in code"
    gate:
      kind: checklist-complete
  - id: fix
    title: Fix
    checklist:
      - "Regression test that fails before the fix, written first"
      - "Minimal fix implemented; no unrelated changes"
    gate:
      kind: checklist-complete
  - id: verify
    title: Verify & Ship
    checklist:
      - "Regression test passes; original repro no longer fails"
      - "Full affected test suite green; docs/changelog updated if user-visible"
    gate:
      kind: none
---
## Phase details

### reproduce
A bug that can't be reproduced can't be safely fixed. Record the exact steps or
command so the fix phase can prove the defect is gone.

### diagnose
Find the *root cause*, not the symptom. A change that only hides the symptom is a
liability; name the real function and reference the evidence.

### fix
Write the failing regression test first, then the smallest fix that makes it pass.
Resist scope creep — a separate concern is a separate task.

### verify
Re-run the repro and the affected suite. If the bug was user-visible, note the
fix in the changelog.
