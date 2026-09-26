"""Slug helpers: derive stable, unique slugs from content paths."""

from __future__ import annotations

import re
from pathlib import Path


def slug_from_filename(path: Path, suffixes: tuple[str, ...] = (".md",)) -> str:
    """`accessibility.agent.md` -> `accessibility`; `foo.bar.agent.md` -> `foo-bar`."""
    name = path.name
    for suffix in sorted(suffixes, key=len, reverse=True):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return _slugify(name)


def slug_from_dir(path: Path) -> str:
    """`skills/acquire-codebase-knowledge/SKILL.md` -> `acquire-codebase-knowledge`."""
    return _slugify(path.parent.name)


def _slugify(raw: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    return slug or "unnamed"
