---
name: test-plan
description: 'Produce a test plan before implementing a feature — what to test, how, and the risks if coverage is thin. Trigger for "write a test plan" or when a Test Engineer scopes a change.'
argument-hint: 'Optional: the feature or module to plan tests for'
---
# Test Plan

Turn a change into a concrete plan of what to test, at which level, and why —
before the code is written.

## Steps
1. **List the behaviors** — enumerate the observable behaviors the change must
   have (including the edge cases: empty, null, boundary, error, concurrent).
2. **Choose the level** for each — unit (fast, isolated), integration (real
   boundaries), or e2e (only where a user-visible contract matters).
3. **Name the test** and the assertion — describe what fails when the behavior breaks.
4. **Note the gaps** — what you are *not* testing and why (cost, flakiness, infra).

## Output shape
| Behavior | Level | Test name | Asserts |
|----------|-------|-----------|---------|

Follow with a short **risks** section: what breaks silently if a listed behavior
goes untested, and the cheapest way to reduce that risk.

Keep the plan proportional — a two-line fix needs a two-line plan, not a matrix.
