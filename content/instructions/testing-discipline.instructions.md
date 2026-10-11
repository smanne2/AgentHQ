---
description: Testing discipline — write and run tests with the change; make them meaningful and fast.
tags: [process, testing]
---
# Testing Discipline

- **Tests ship with the code** — add or update tests in the same change as the
  behavior; never "tests later".
- **Test the contract, not the implementation** — assert on observable behavior.
- **Cover the interesting paths**: empty/null/boundary/error, not just the happy path.
- **Make them pass before declaring done** — run the relevant tests and report results.
- **Keep the suite fast** — unit tests default; integration tests only when needed.
  If a test is flaky or slow, fix it or annotate it explicitly.
- Match the project's existing framework, layout, and naming — don't introduce a
  new test style mid-repo.
