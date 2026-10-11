---
description: Python conventions — typed, tested, idiomatic; ruff-clean; explicit boundaries.
applyTo: ['**/*.py', 'pyproject.toml', 'requirements.txt', 'setup.py']
tags: [python, convention]
---
# Python Conventions

- **Type-hint public interfaces** — functions and classes get parameter and return
  annotations; use `mypy`/`pyright`-clean types.
- **Idiomatic** — prefer the standard library; PEP 8; f-strings; `pathlib` over
  `os.path`; context managers for resources.
- **No bare `except`** — catch specific exceptions; don't swallow without a reason.
- **Tests with pytest** — colocate or mirror the package layout; use fixtures, not
  setup/teardown boilerplate.
- **Keep it ruff-clean** — run the formatter/linter before finishing.
- **Config via env** — read settings from the environment with a typed model.
