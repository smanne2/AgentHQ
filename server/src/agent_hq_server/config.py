"""Runtime configuration: environment variables and CLI flags (technical.md §2.1).

Everything here is overridable via env so the same image works for any
content tree; ``__main__`` turns flags into a fully built ``Config``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _expand(path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path)))


def default_content_path() -> Path:
    """``AGENT_HQ_CONTENT`` if set, else ``<repo>/content`` next to the install."""
    env = os.environ.get("AGENT_HQ_CONTENT")
    if env:
        return _expand(env)
    return Path(__file__).resolve().parents[2] / "content"


def default_project_path() -> Path:
    """``AGENT_HQ_PROJECT`` if set, else the process CWD (technical.md R2)."""
    env = os.environ.get("AGENT_HQ_PROJECT")
    return _expand(env) if env else Path.cwd()


def resolve_project_path(raw: str | None) -> Path | None:
    """Explicit argument > env/flag default. Never infers silently elsewhere."""
    if raw:
        return _expand(raw)
    env = os.environ.get("AGENT_HQ_PROJECT")
    return _expand(env) if env else None


@dataclass
class Config:
    """Fully-resolved runtime config; ``build`` resolves every default."""

    content_path: Path = field(default_factory=default_content_path)
    project_path: Path | None = None
    log_level: str = "INFO"

    def project_or_cwd(self) -> Path:
        return self.project_path or Path.cwd()

    @property
    def profile_pin_file(self) -> Path:
        """Pinned profile for the target project (read by bootstrap)."""
        return self.project_or_cwd() / ".agent-hq" / "profile.yaml"


def build(
    content_path: str | None = None,
    project_path: str | None = None,
    log_level: str | None = None,
) -> Config:
    """Flag > env > default, for every setting."""
    return Config(
        content_path=_expand(content_path) if content_path else default_content_path(),
        project_path=resolve_project_path(project_path),
        log_level=log_level or os.environ.get("AGENT_HQ_LOG_LEVEL", "INFO"),
    )
