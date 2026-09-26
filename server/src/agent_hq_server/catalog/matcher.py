"""Profile selection and instruction matching (technical.md §4.5).

Selection order: pinned profile id > best-scoring auto match > ``default``
fallback. "Signals" are project manifest files as ``{basename: text}`` —
Phase 3's ``detect.py`` produces them; tests can build them by hand.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

import pathspec
from pydantic import BaseModel, ConfigDict

from agent_hq_server.catalog.catalog import Catalog, ProfileItem
from agent_hq_server.schema import FileMatch, Profile

ProfileSource = "pinned" | "auto" | "fallback"


def pick_profile(
    catalog: Catalog,
    pinned_id: str | None = None,
    signals: Mapping[str, str] | None = None,
) -> tuple[ProfileItem, ProfileSource]:
    """Return ``(profile_item, source)`` where source is pinned|auto|fallback."""
    profiles = catalog.profiles
    if pinned_id:
        for item in profiles:
            if item.frontmatter.id == pinned_id:
                return item, "pinned"
    if signals:
        best = None
        best_score = 0
        for item in profiles:
            score = _score(item.frontmatter, signals)
            if score > best_score:
                best, best_score = item, score
        if best is not None:
            return best, "auto"
    for item in profiles:
        if item.frontmatter.id == "default":
            return item, "fallback"
    if profiles:
        return profiles[0], "fallback"
    raise LookupError("no profiles available in the content tree")


def _score(profile: Profile, signals: Mapping[str, str]) -> int:
    matches = profile.matches
    if matches is None or (not matches.any_of and not matches.all_of):
        return 0
    if matches.all_of and not all(
        _rule_matches(rule, signals) for rule in matches.all_of
    ):
        return 0
    any_hits = sum(1 for rule in matches.any_of if _rule_matches(rule, signals))
    return any_hits if matches.any_of else (1 if matches.all_of else 0)


def _rule_matches(rule: FileMatch, signals: Mapping[str, str]) -> bool:
    text = signals.get(rule.file)
    if text is None:
        return False
    if not rule.contains_any:
        return True  # mere file presence
    return any(needle in text for needle in rule.contains_any)


def match_instructions(
    instructions: Iterable[Instruction],
    file_patterns: list[str] | None = None,
    tag: str | None = None,
) -> list[Instruction]:
    """Select instructions for a project.

    No ``applyTo`` = global rule (always included). With ``applyTo``, the
    instruction is included when any glob matches any project file path.
    """
    patterns = list(file_patterns or [])
    selected: list[Instruction] = []
    for item in instructions:
        if tag is not None and (
            item.frontmatter.tags is None or tag not in item.frontmatter.tags
        ):
            continue
        globs = item.frontmatter.apply_to or []
        if not globs or _any_glob_matches(globs, patterns):
            selected.append(item)
    return selected


def _any_glob_matches(globs: list[str], patterns: list[str]) -> bool:
    if not patterns:
        return False
    spec = pathspec.PathSpec.from_lines("gitwildmatch", globs)
    return any(spec.match_file(pattern) for pattern in patterns)


class BundleMatchInput(BaseModel):
    """Typed input for bundle assembly (used by the bootstrap tool in Phase 2/3)."""

    model_config = ConfigDict(extra="allow")

    project_path: str
    pinned_profile: str | None = None
    signals: dict[str, str] = {}
    file_patterns: list[str] = []
