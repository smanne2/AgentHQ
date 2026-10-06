---
description: TypeScript conventions — strict mode, no `any`, named exports, explicit types at boundaries.
applyTo: ['**/*.ts', '**/*.tsx', '**/*.mts', 'tsconfig.json']
tags: [typescript, convention]
---
# TypeScript Conventions

- **Strict mode on** — `strict: true` in `tsconfig.json`; no new `@ts-ignore`
  without a comment explaining why.
- **No `any`** — use `unknown` + narrowing, generics, or a real type. A deliberate
  boundary escape gets a comment.
- **Explicit types at boundaries** — public functions, API payloads, and props have
  explicit types; locals may use inference.
- **Named exports** — prefer named over default exports for reusability and renaming.
- **Errors** — throw typed errors or Result-style returns; don't leak `catch` blocks
  that swallow without a reason.
- Keep `enum` usage minimal; prefer string literal unions.
