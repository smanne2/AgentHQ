# Inquiry Checkpoints

Per-document question list. Answer each with a file/config reference; mark
unknowns `[TODO]` and intent gaps `[ASK USER]`.

## STACK.md
- What language(s), runtime version(s), and major frameworks/libraries are present?
- What are the top-level dependencies, and which are production vs. dev?
- What build/package manager is used?

## STRUCTURE.md
- What is the top-level directory layout, and what does each area hold?
- Where are the entry points (server, CLI, main)?
- Which files are generated vs. source?

## ARCHITECTURE.md
- What are the layers/modules and how do they communicate?
- Where is state stored, and what is the data flow for a typical request/task?
- What design patterns dominate (note where they actually appear)?

## CONVENTIONS.md
- Naming, formatting, import style, and error-handling patterns in use.
- Linter/formatter config and how it's invoked.

## INTEGRATIONS.md
- External APIs, databases, message queues, auth providers, and monitoring.
- How are credentials/config supplied (env vars, files)?

## TESTING.md
- Test framework(s), where tests live, and how they're run.
- Mocking strategy and coverage tooling, if any.

## CONCERNS.md
- Technical debt, known bugs, security risks, and performance bottlenecks.
- Highest-churn files (from git history) as fragility signals.
