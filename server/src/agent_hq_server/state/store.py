"""Atomic JSON state persistence for project workflows (technical.md §6.1).

States are per-project+workflow, stored in ~/.agent-hq/state/
using a hash of the project path to keep filenames stable and safe.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


def _get_state_dir() -> Path:
    """Returns the standard state directory ~/.agent-hq/state/."""
    path = Path("~/.agent-hq/state").expanduser()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _project_hash(project_path: Path) -> str:
    """Deterministic hash of project path for filename safety."""
    return hashlib.sha256(str(project_path.resolve()).encode()).hexdigest()[:16]


def save_state(project_path: Path, workflow_slug: str, state: dict[str, Any]) -> None:
    """Saves workflow state atomically (tmp + rename)."""
    state_dir = _get_state_dir()
    filename = f"{_project_hash(project_path)}-{workflow_slug}.json"
    path = state_dir / filename
    tmp_path = path.with_suffix(".tmp")

    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        tmp_path.replace(path)
    except OSError as exc:
        log.error("failed to save state %s: %s", path, exc)
        raise


def load_state(project_path: Path, workflow_slug: str) -> dict[str, Any]:
    """Loads workflow state or returns empty dict if not found."""
    state_dir = _get_state_dir()
    filename = f"{_project_hash(project_path)}-{workflow_slug}.json"
    path = state_dir / filename

    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        log.error("failed to load state %s: %s", path, exc)
        return {}
