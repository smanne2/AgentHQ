#!/usr/bin/env python3
"""Fail if any source file exceeds the 300-line budget (plan rule G6).

Documents and content files are exempt; only Python source/test files are
scanned. Run from anywhere: `python server/scripts/check_lines.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

LIMIT = 300
SCAN_DIRS = (
    "server/src",
    "server/tests",
    "server/scripts",
    "cli/src",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def main() -> int:
    root = _repo_root()
    offenders: list[str] = []
    checked = 0
    for name in SCAN_DIRS:
        base = root / name
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.py")):
            lines = len(path.read_text(encoding="utf-8").splitlines())
            checked += 1
            if lines > LIMIT:
                offenders.append(f"  {path.relative_to(root)}: {lines} lines")
    if offenders:
        print(f"FAIL: {len(offenders)} file(s) exceed {LIMIT} lines:")
        print("\n".join(offenders))
        return 1
    print(f"OK: {checked} source file(s), all within {LIMIT} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
