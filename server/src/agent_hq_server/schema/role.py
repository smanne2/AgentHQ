"""Role — an agent persona. Maps 1:1 to awesome-copilot ``agents/*.agent.md``."""

from __future__ import annotations

from pydantic import ConfigDict, Field

from agent_hq_server.schema.common import ContentBase


class RoleFrontmatter(ContentBase):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    name: str | None = None
    # Client-specific passthrough keys (Copilot agents set both):
    model: str | None = Field(
        default=None,
        description="Optional client/model hint (passthrough, not enforced)",
    )
    tools: list[str] | None = Field(
        default=None,
        description="Optional client tool list (passthrough, not enforced)",
    )
