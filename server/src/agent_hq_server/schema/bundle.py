"""Return shapes for ``agent_hq.bootstrap`` and the ``list_*`` tools (technical.md §5).

Token-efficiency rule G5: summaries carry slugs + one-liners; full markdown
travels via ``get_*`` — except the bundle, which inlines instruction bodies
(they are small and needed immediately).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from agent_hq_server.schema.workflow import Gate


class RoleSummary(BaseModel):
    slug: str
    name: str | None = None
    description: str


class InstructionSummary(BaseModel):
    slug: str
    description: str
    apply_to: list[str] | None = None


class SkillSummary(BaseModel):
    slug: str
    description: str
    files: list[str] = Field(default_factory=list)


class InstructionView(BaseModel):
    """Full instruction text (inlined in the bootstrap bundle)."""

    slug: str
    description: str
    body: str


class PhaseView(BaseModel):
    id: str
    title: str
    checklist: list[str] = Field(default_factory=list)
    gate: Gate = Field(default_factory=Gate)


class WorkflowView(BaseModel):
    slug: str
    name: str | None = None
    description: str
    phases: list[PhaseView] = Field(default_factory=list)


class BundleProfile(BaseModel):
    id: str
    name: str | None = None
    source: Literal["pinned", "auto", "fallback"]


class Bundle(BaseModel):
    """What ``agent_hq.bootstrap`` returns (technical.md §5.1)."""

    model_config = ConfigDict(extra="allow")

    content_version: str
    profile: BundleProfile
    workflow: WorkflowView | None = None
    instructions: list[InstructionView] = Field(default_factory=list)
    roles: list[RoleSummary] = Field(default_factory=list)
    skills: list[SkillSummary] = Field(default_factory=list)
    next_action: str
