"""Path resolution for the CLI: locate the Agent HQ checkout from the installed package.

Editable workspace installs point `agent_hq_server` at `server/src/…`, so the
repo root is three levels up; a real sdist/wheel install has no repo next to it,
in which case the `AGENT_HQ_ROOT` env var is the escape hatch (R2-style).
"""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    """Absolute path of the Agent HQ repository (where `uv run` must execute)."""
    env = os.environ.get("AGENT_HQ_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(agent_hq_root_pkg_file()).resolve().parents[3]


def agent_hq_root_pkg_file() -> Path:
    """A file inside the installed `agent_hq_server` package (import-safe)."""
    import agent_hq_server

    return Path(agent_hq_server.__file__)


def content_root() -> Path:
    """Default content tree: `AGENT_HQ_CONTENT` env, else `<repo>/content`."""
    env = os.environ.get("AGENT_HQ_CONTENT")
    if env:
        return Path(env).expanduser().resolve()
    return repo_root() / "content"


def templates_root() -> Path:
    """The `client/templates/` directory shipped with the repo."""
    return repo_root() / "client" / "templates"
