"""Read the project's pinned profile (``.agent-hq/profile.yaml``).

The pin file is a small YAML with ``profile: <id>`` — the only input of the
bootstrap handshake besides ``projectPath`` (technical.md §3.1). A missing or
unreadable file is never an error: bootstrap simply falls back to detection.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

import yaml

PIN_RELPATH = ".agent-hq/profile.yaml"


def read_pin_file(
    project_path: Path, env: Mapping[str, str] | None = None
) -> tuple[str | None, str | None]:
    """Return ``(pinned_profile_id, warning)`` for the given project directory.

    ``env`` defaults to ``os.environ``; tests inject it. The env var
    ``AGENT_HQ_PROFILE`` overrides the file pin (handy for one-off runs).
    """
    env = os.environ if env is None else env
    override = env.get("AGENT_HQ_PROFILE", "").strip()
    if override:
        return override, None

    pin_file = project_path / PIN_RELPATH
    if not pin_file.is_file():
        return None, None
    try:
        data = yaml.safe_load(pin_file.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return None, f"{pin_file}: unreadable pin file ({exc}); using detection"
    if not isinstance(data, dict):
        return None, None
    profile = data.get("profile")
    if not isinstance(profile, str) or not profile.strip():
        return None, None
    return profile.strip(), None
