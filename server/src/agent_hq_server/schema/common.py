"""Shared base for markdown frontmatter models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ContentBase(BaseModel):
    """Base for all markdown frontmatter.

    ``extra="allow"`` keeps unknown keys (and ``protected_namespaces=()``
    allows client-specific keys like ``model``) so awesome-copilot files
    import with zero rework even as that repo evolves (technical.md R3/DD4).
    """

    model_config = ConfigDict(extra="allow", protected_namespaces=())

    description: str = Field(min_length=1)
    tags: list[str] | None = None
