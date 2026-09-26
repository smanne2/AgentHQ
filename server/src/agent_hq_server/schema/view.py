"""On-demand tool return views (technical.md §5 ``get_*`` + list rows).

These are tool-layer shapes, not content models: pydantic so FastMCP
derives each tool's output schema from the typed return annotation.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorView(BaseModel):
    """Returned by ``get_*`` tools when the slug is unknown (R3)."""

    error: str
    known_slugs: list[str] = Field(default_factory=list)


class RoleView(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    slug: str
    name: str | None = None
    description: str
    model: str | None = None
    tools: list[str] | None = None
    tags: list[str] | None = None
    body: str


class InstructionViewFull(BaseModel):
    model_config = ConfigDict(extra="allow")

    slug: str
    description: str
    apply_to: list[str] | None = None
    tags: list[str] | None = None
    convention: bool = False
    body: str


class SkillView(BaseModel):
    model_config = ConfigDict(extra="allow")

    slug: str
    name: str | None = None
    description: str
    files: list[str] = Field(default_factory=list)  # sibling manifest, paths only
    body: str


class WorkflowSummary(BaseModel):
    """Row for ``list_workflows``: phases as {id,title} pairs only (G5)."""

    slug: str
    name: str | None = None
    description: str
    phases: list[dict[str, str]] = Field(default_factory=list)


class ChecklistView(BaseModel):
    """Single-phase view of a workflow: what to do + what gates it."""

    slug: str
    phase_id: str
    title: str
    checklist: list[str] = Field(default_factory=list)
    gate: dict[str, Any] = Field(default_factory=dict)
    next_after_pass: str | None = None  # id of the following phase, else null
    body_section: str | None = None


class WorkflowViewFull(BaseModel):
    model_config = ConfigDict(extra="allow")

    slug: str
    name: str | None = None
    description: str
    version: str | None = None
    phases: list[dict[str, Any]] = Field(default_factory=list)
    body: str


class Counts(BaseModel):
    model_config = ConfigDict(extra="allow")

    roles: int
    instructions: int
    skills: int
    workflows: int
    profiles: int


class ContentInfoView(BaseModel):
    """``agent_hq.content_info`` — staleness detection + tree overview."""

    content_version: str
    counts: Counts
    profile_ids: list[str] = Field(default_factory=list)
    content_root: str | None = None
