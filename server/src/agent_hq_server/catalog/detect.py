"""Stack detection from project manifest files.

Returns a mapping of manifest filename to file contents. These signals are
used by the matcher to pick a profile (technical.md §4.5).
"""

from __future__ import annotations

import contextlib
from pathlib import Path


def detect_stack(project_path: Path) -> dict[str, str]:
    """Detect the project stack from manifest files in project_path.

    Reads common manifest files (package.json, pyproject.toml, go.mod, etc.)
    and returns a dict of {filename: content}. Returns empty dict if no
    manifests are found.
    """
    signals: dict[str, str] = {}

    # Try common manifest files in order of preference
    manifest_files = [
        "package.json",
        "pyproject.toml",
        "go.mod",
        "Cargo.toml",
        "Pipfile",
        "Pipfile.lock",
        "requirements.txt",
        "Pipfile.lock",
        "composer.json",
        "gradle.properties",
        "pom.xml",
        "build.gradle",
        "Dockerfile",
    ]

    for manifest in manifest_files:
        manifest_path = project_path / manifest
        if manifest_path.is_file():
            with contextlib.suppress(Exception):  # unreadable file: skip it
                signals[manifest] = manifest_path.read_text(encoding="utf-8")

    return signals
