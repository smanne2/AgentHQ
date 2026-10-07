# Contributing to Agent HQ

## Adding Content
Agent HQ uses a simple markdown-based system. All content files must have YAML frontmatter.

### Roles (`content/agents/*.agent.md`)
- `name`: Display name.
- `description`: Persona description.
- `model`: Optional model override.

### Instructions (`content/instructions/*.instructions.md`)
- `description`: What the instruction does.
- `apply_to`: Glob pattern for files this instruction applies to.

### Workflows (`content/workflows/*.workflow.md`)
Workflows are phased. Each phase has:
- `id`: Kebab-case identifier.
- `checklist`: List of requirements.
- `gate`: The condition for passing (manual, artifact, checklist-complete, or none).

## Validation
Run the validation tool before submitting PRs:
```bash
uv run agent-hq validate
```
CI will enforce that all source files are $\le$ 300 lines.
