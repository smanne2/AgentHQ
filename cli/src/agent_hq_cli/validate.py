"""`agent-hq validate [path]` — schema-check the entire content tree.

Loads every content file through the catalog (frontmatter + pydantic validation)
and reports any issues. The contributor gate: exit 0 only when the tree is clean.
"""

from __future__ import annotations

from pathlib import Path

from agent_hq_server.catalog.catalog import load

from agent_hq_cli.config import content_root


def run_validate(path: Path | None) -> int:
    tree = (path or content_root()).resolve()
    if not tree.is_dir():
        print(f"✗ content tree not found: {tree}")
        return 2

    catalog = load(tree)
    counts = catalog.counts()
    print(f"content tree: {tree}")
    print(
        f"  roles={counts['role']} instructions={counts['instruction']} "
        f"skills={counts['skill']} workflows={counts['workflow']} "
        f"profiles={counts['profile']} version={catalog.version[:12]}"
    )

    if not catalog.profiles:
        print("  ✗ no profiles found — bootstrap would have nothing to fall back to")
        return 1

    if catalog.issues:
        print(f"\n✗ {len(catalog.issues)} issue(s) found:")
        for issue in catalog.issues:
            print(f"  - {issue.render()}")
        return 1

    print("\n✓ validate: content tree is clean")
    return 0
