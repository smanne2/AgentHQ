"""``agent_hq.bootstrap`` — the session-start handshake (technical.md §3.1).

Assembly pipeline: pin file → stack detection (``catalog/detect.py``) →
profile pick (``catalog/matcher.py``) → bundle (``catalog/bundle.py``).
"""

from __future__ import annotations

import logging
from pathlib import Path

from agent_hq_server.catalog.bundle import assemble_bundle
from agent_hq_server.catalog.catalog import Catalog
from agent_hq_server.catalog.detect import detect_stack
from agent_hq_server.catalog.matcher import pick_profile
from agent_hq_server.catalog.pin import read_pin_file
from agent_hq_server.schema import Bundle, ErrorView

log = logging.getLogger(__name__)

_SCAN_IGNORED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
}


def bootstrap(
    catalog: Catalog,
    project_path: Path,
    pinned_profile: str | None = None,
) -> Bundle | ErrorView:
    """Resolve the project's onboarding bundle.

    Profile selection (technical.md §4.5): explicit ``pinned_profile`` arg >
    ``.agent-hq/profile.yaml`` pin > auto-detect from manifest signals >
    ``default`` fallback.
    """
    file_pin, pin_warning = read_pin_file(project_path)
    effective_pin = pinned_profile or file_pin

    try:
        profile, source = pick_profile(
            catalog,
            pinned_id=effective_pin,
            signals=detect_stack(project_path),
        )
    except LookupError as exc:
        return ErrorView(
            error=f"profile selection failed: {exc}; add a profiles/ file to the content tree"
        )

    warnings = [pin_warning] if pin_warning else []
    file_patterns = _project_file_patterns(project_path)
    bundle = assemble_bundle(catalog, profile, source, file_patterns, warnings)
    if warnings:
        bundle.warnings = warnings  # type: ignore[attr-defined]  # extra="allow" field
    return bundle


def _project_file_patterns(project_path: Path) -> list[str]:
    """Relative POSIX paths of the project's files, for ``applyTo`` matching.

    Vendor/hidden trees are pruned and unreadable dirs skipped: the scan
    feeds glob matching only, never content.
    """
    if not project_path.is_dir():
        return []
    patterns: list[str] = []
    try:
        for path in project_path.rglob("*"):
            if path.is_file() and all(part not in _SCAN_IGNORED_DIRS for part in path.parts):
                patterns.append(path.relative_to(project_path).as_posix())
    except OSError:
        return []
    return patterns
