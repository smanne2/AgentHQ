"""Workflow — Agent HQ's original type: a phased process with checklists and gates.

awesome-copilot has no dev-process workflow type (its ``workflows/`` holds
repo-ops reports), so the phase structure here is ours (technical.md §4.4).
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from agent_hq_server.schema.common import ContentBase

GateKind = Literal["none", "manual", "artifact", "checklist-complete"]
_ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]*")


class Gate(BaseModel):
    """What must be true before the next phase may start (technical.md §4.4)."""

    model_config = ConfigDict(extra="allow")

    kind: GateKind = "none"
    pattern: str | None = None

    @model_validator(mode="after")
    def _artifact_needs_pattern(self) -> Gate:
        if self.kind == "artifact" and not self.pattern:
            raise ValueError("gate kind 'artifact' requires a pattern")
        return self


class Phase(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    title: str | None = None
    checklist: list[str] = Field(default_factory=list)
    gate: Gate = Field(default_factory=Gate)

    @field_validator("id")
    @classmethod
    def _kebab_id(cls, value: str) -> str:
        if not _ID_PATTERN.fullmatch(value):
            raise ValueError("phase id must be kebab-case, e.g. 'design'")
        return value

    @property
    def display_title(self) -> str:
        return self.title or self.id.replace("-", " ").title()


class WorkflowFrontmatter(ContentBase):
    name: str | None = None
    version: str | None = None
    phases: list[Phase] = Field(min_length=1)

    @model_validator(mode="after")
    def _unique_phase_ids(self) -> WorkflowFrontmatter:
        seen: set[str] = set()
        for phase in self.phases:
            if phase.id in seen:
                raise ValueError(f"duplicate phase id '{phase.id}'")
            seen.add(phase.id)
        return self
