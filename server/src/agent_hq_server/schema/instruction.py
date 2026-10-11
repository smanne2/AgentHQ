"""Instruction — standing rules. Maps to awesome-copilot ``instructions/*.instructions.md``.

Conventions (``content/conventions/``) reuse this schema; they are
instructions with a ``convention``/stack tag (technical.md DD5).
"""

from __future__ import annotations

from pydantic import ConfigDict, Field, field_validator

from agent_hq_server.schema.common import ContentBase


class InstructionFrontmatter(ContentBase):
    model_config = ConfigDict(
        extra="allow", protected_namespaces=(), populate_by_name=True
    )

    # awesome-copilot spells the key `applyTo` (camelCase) in YAML:
    apply_to: list[str] | None = Field(default=None, alias="applyTo")

    @field_validator("apply_to", mode="before")
    @classmethod
    def _normalize_apply_to(cls, raw: object) -> list[str] | None:
        """Accept a glob, a comma-separated glob list, or a YAML list."""
        if raw is None:
            return None
        if isinstance(raw, str):
            return [part.strip() for part in raw.split(",") if part.strip()]
        if isinstance(raw, list):
            return [str(item).strip() for item in raw if str(item).strip()]
        raise ValueError("applyTo must be a string or a list of strings")
