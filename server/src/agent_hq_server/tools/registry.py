"""MCP tool registry — the second of two ``mcp`` SDK touchpoints (DD10).

Names follow the ``agent_hq.*`` scheme from technical.md §5 (dots are legal
per MCP SEP-986). JSON keys follow the design's camelCase contract
(``projectPath``, ``workflowSlug`` …): multi-word parameters carry a
pydantic alias, single words stay as-is. Handler args are plain values, so
the semantics live in the unit-tested ``tools/*`` modules; the registry
itself is covered by a stdio round-trip test (test_mcp_stdio.py).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from agent_hq_server.catalog.catalog import load
from agent_hq_server.config import Config
from agent_hq_server.tools import bootstrap as bootstrap_mod
from agent_hq_server.tools import content_info as content_info_mod
from agent_hq_server.tools import instructions as instructions_mod
from agent_hq_server.tools import roles as roles_mod
from agent_hq_server.tools import skills as skills_mod
from agent_hq_server.tools import workflows as workflows_mod

log = logging.getLogger(__name__)

INSTRUCTIONS = (
    "Agent HQ serves agent guidance from a git-versioned content tree: roles, "
    "instructions, skills, and phased workflows. First action of a session in "
    "any project: call agent_hq.bootstrap with the project path, then follow "
    "the returned workflow — phases in order, one at a time."
)


def create_server(config: Config) -> FastMCP:
    """Build the FastMCP instance with all tools wired to ``config``'s catalog."""
    catalog = load(config.content_path)
    log.info(
        "content tree %s: version %s, counts %s, issues %d",
        config.content_path,
        catalog.version,
        catalog.counts(),
        len(catalog.issues),
    )
    if config.project_path is None:
        log.info("no project path (AGENT_HQ_PROJECT unset); bootstrap will use CWD")

    mcp = FastMCP(name="agent-hq", instructions=INSTRUCTIONS)

    @mcp.tool(name="agent_hq.bootstrap")
    def bootstrap(
        projectPath: Annotated[str, Field(alias="projectPath")],
        pinnedProfile: Annotated[str | None, Field(alias="pinnedProfile")] = None,
    ) -> dict[str, Any]:
        """Session start: return this project's onboarding bundle.

        Resolves the profile (pinned > detected > fallback) and returns the
        workflow with all phases/checklists/gates, inlined instruction
        bodies, role roster, and skills. Call once per session, first.
        """
        path = Path(projectPath).expanduser().resolve()
        result = bootstrap_mod.bootstrap(catalog, path, pinned_profile=pinnedProfile)
        return _dump(result)

    @mcp.tool(name="agent_hq.content_info")
    def content_info() -> dict[str, Any]:
        """Content tree overview: version digest, per-kind counts, profile ids."""
        return _dump(content_info_mod.content_info(catalog))

    @mcp.tool(name="agent_hq.list_roles")
    def list_roles(tag: str | None = None) -> dict[str, Any]:
        """List available roles (slug, name, one-line description)."""
        return {"roles": _dump(roles_mod.list_roles(catalog, tag=tag))}

    @mcp.tool(name="agent_hq.get_role")
    def get_role(slug: str) -> dict[str, Any]:
        """Full role: persona prompt body + passthrough fields."""
        return _dump(roles_mod.get_role(catalog, slug))

    @mcp.tool(name="agent_hq.list_instructions")
    def list_instructions(tag: str | None = None, convention: bool | None = None) -> dict[str, Any]:
        """List instructions (and conventions, which are tagged instructions)."""
        return {
            "instructions": _dump(
                instructions_mod.list_instructions(catalog, tag=tag, convention=convention)
            )
        }

    @mcp.tool(name="agent_hq.get_instruction")
    def get_instruction(slug: str) -> dict[str, Any]:
        """Full instruction text (markdown body)."""
        return _dump(instructions_mod.get_instruction(catalog, slug))

    @mcp.tool(name="agent_hq.list_skills")
    def list_skills() -> dict[str, Any]:
        """List skills (slug, description, sibling file manifest)."""
        return {"skills": _dump(skills_mod.list_skills(catalog))}

    @mcp.tool(name="agent_hq.get_skill")
    def get_skill(slug: str) -> dict[str, Any]:
        """Full skill body + sibling file manifest (paths only; never executed)."""
        return _dump(skills_mod.get_skill(catalog, slug))

    @mcp.tool(name="agent_hq.list_workflows")
    def list_workflows() -> dict[str, Any]:
        """List workflows (slug, name, description, phase ids/titles)."""
        return {"workflows": _dump(workflows_mod.list_workflows(catalog))}

    @mcp.tool(name="agent_hq.get_workflow")
    def get_workflow(
        slug: str, phaseId: Annotated[str | None, Field(alias="phaseId")] = None
    ) -> dict[str, Any]:
        """Full workflow (all phases), or a single phase's checklist + gate."""
        return _dump(workflows_mod.get_workflow(catalog, slug, phase_id=phaseId))

    @mcp.tool(name="agent_hq.get_checklist")
    def get_checklist(
        workflowSlug: Annotated[str, Field(alias="workflowSlug")],
        phaseId: Annotated[str, Field(alias="phaseId")],
    ) -> dict[str, Any]:
        """Checklist for one workflow phase + its gate + what follows it."""
        return _dump(workflows_mod.get_checklist(catalog, workflowSlug, phaseId))

    return mcp


def _dump(value: object) -> Any:
    """Serialize a pydantic view (or list of them) to plain JSON-able data."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_dump(v) for v in value]
    model = getattr(value, "model_dump", None)
    if model is not None:
        return model(mode="json", exclude_none=True)
    raise TypeError(f"not serializable as an MCP tool result: {type(value).__name__}")
