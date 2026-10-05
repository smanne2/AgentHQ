"""Stack detection from project manifest files.

Returns a mapping of manifest filename to file contents. These signals are
used by the matcher to pick a profile (technical.md §4.5).
"""

from __future__ import annotations

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
            try:
                signals[manifest] = manifest_path.read_text(encoding="utf-8")
            except Exception:
                # If we can't read the file, skip it
                pass

    return signals


def detect_stack_from_signals(signals: dict[str, str]) -> str:
    """Determine the primary stack from manifest signals.

    Returns a string like "node", "python", "go", "rust", etc.
    If multiple stacks are detected, returns the most specific one.
    Returns "unknown" if no stack can be determined.
    """
    # Check for Node.js (package.json is most specific indicator)
    if "package.json" in signals:
        content = signals["package.json"]
        if "typescript" in content.lower() or "ts-node" in content.lower():
            return "typescript"
        return "node"

    # Check for Python
    if "pyproject.toml" in signals:
        content = signals["pyproject.toml"]
        if "[tool.poetry]" in content or "[tool.brew]" in content:
            return "python-poetry"
        return "python"

    if "requirements.txt" in signals:
        return "python-requirements"

    # Check for Go
    if "go.mod" in signals:
        return "go"

    # Check for Rust
    if "Cargo.toml" in signals:
        return "rust"

    # Check for PHP
    if "composer.json" in signals:
        return "php"

    # Check for Java
    if "pom.xml" in signals or "build.gradle" in signals:
        return "java"

    # Check for Pipenv
    if "Pipfile" in signals:
        return "python-pipenv"

    return "unknown"
