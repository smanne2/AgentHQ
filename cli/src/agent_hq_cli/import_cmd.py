"""`agent-hq import <path>` — bring community content (e.g. awesome-copilot) in.

Discovers agent/instruction/skill/workflow/profile files under a source path and
reports where each would land in the content tree. Default is a **dry-run** (nothing
copied); pass `--copy` to write. Schemas already accept community frontmatter, so
this copies files verbatim — no normalization (R3).
"""

from __future__ import annotations

import shutil
from pathlib import Path

_KIND_BY_SUFFIX = {
    ".agent.md": "agents",
    ".instructions.md": "instructions",
    ".workflow.md": "workflows",
    ".profile.yaml": "profiles",
}


def _relative_target(src: Path, source: Path) -> Path | None:
    """Map a source file to its path *under* the content tree, or None if ignored."""
    if src.name == "SKILL.md" and src.parent != source:
        return Path("skills") / src.parent.name / "SKILL.md"
    for suffix, subdir in _KIND_BY_SUFFIX.items():
        if src.name.endswith(suffix):
            return Path(subdir) / src.name
    return None


def _discover(source: Path) -> list[tuple[Path, Path]]:
    """Return (source_file, relative_target_under_content) for recognized files."""
    items: list[tuple[Path, Path]] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        target = _relative_target(path, source)
        if target is not None:
            items.append((path, target))
    return items


def run_import(source: Path, target: Path, copy: bool) -> int:
    source = source.expanduser().resolve()
    target = (target or Path("content")).expanduser().resolve()
    if not source.is_dir():
        print(f"✗ source not found: {source}")
        return 2

    items = _discover(source)
    if not items:
        print(f"no recognizable content files under {source}")
        return 1

    verb = "would copy" if not copy else "copied"
    collisions = 0
    for src, rel in items:
        dest = target / rel
        exists = dest.exists()
        action = verb if not exists else ("would skip" if not copy else "overwrite")
        mark = "  ! " if exists else "  "
        print(f"{mark}{action}: {src.relative_to(source)} -> {rel}")
        if exists:
            collisions += 1
        if copy and not exists:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

    print(
        f"\n{'✓ imported' if copy else '✓ dry-run'}: "
        f"{len(items)} file(s), {collisions} collision(s)"
    )
    if not copy and items:
        print("  (pass --copy to actually copy)")
    return 0
