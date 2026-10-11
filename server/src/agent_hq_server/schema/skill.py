"""Skill — reusable task playbook. Maps to awesome-copilot ``skills/<name>/SKILL.md``.

``license``/``compatibility``/``metadata``/``argument-hint`` stay passthrough
extras. Sibling files (``scripts/``, ``references/``) are surfaced by the
tools layer, not the schema.
"""

from __future__ import annotations

from agent_hq_server.schema.common import ContentBase


class SkillFrontmatter(ContentBase):
    name: str | None = None  # display name; slug always comes from the directory
