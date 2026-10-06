---
description: Node.js API conventions — layered request handling, validated input, structured errors.
applyTo: ['**/*.ts', '**/*.js', '**/*.mts', '**/*.cjs', 'package.json']
tags: [node, convention]
---
# Node API Conventions

- **Layers** — route handler → service → data access. Handlers parse/validate input
  and map results to responses; business logic lives in services.
- **Validate input at the edge** — use a schema (zod/joi/ajv) for every external
  input; fail fast with a 4xx on invalid payloads.
- **Structured errors** — a shared error type with `code`, `message`, and `status`;
  a single error-handling middleware turns it into a consistent response.
- **Async** — always `await`; wrap handlers so rejected promises become responses,
  not unhandled rejections.
- **Config** — read from the environment with a typed loader; never hardcode values.
- **Dependency injection** — pass dependencies in where feasible so services are testable.
