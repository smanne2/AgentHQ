"""Content tree versioning: a short, stable digest of the content directory."""

from __future__ import annotations

import hashlib
from pathlib import Path


def content_digest(root: Path) -> str:
    """SHA-256 over (relative path, bytes) of every file, sorted by path.

    Stable across filesystems; changes iff content changes. Returned as a
    10-character hex prefix (the `contentVersion` agents see at bootstrap).
    """
    if not root.is_dir():
        return "missing"
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()[:10]
