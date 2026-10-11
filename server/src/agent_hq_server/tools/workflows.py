"""``agent_hq.list_workflows`` / ``get_workflow`` / ``get_checklist`` handlers."""

from __future__ import annotations

import logging

from agent_hq_server.catalog.catalog import Catalog, Workflow
from agent_hq_server.schema import (
    ChecklistView,
    ErrorView,
    WorkflowSummary,
    WorkflowViewFull,
)

log = logging.getLogger(__name__)


def list_workflows(catalog: Catalog) -> list[WorkflowSummary]:
    """G5: slug + name + description; phase ids/titles only (no checklists)."""
    return [
        WorkflowSummary(
            slug=w.slug,
            name=w.frontmatter.name,
            description=w.frontmatter.description,
            phases=[
                {"id": p.id, "title": p.display_title} for p in w.frontmatter.phases
            ],
        )
        for w in catalog.workflows
    ]


def get_workflow(
    catalog: Catalog, slug: str, phase_id: str | None = None
) -> WorkflowViewFull | ChecklistView | ErrorView:
    """Full workflow (all phases + body), or a single-phase checklist view."""
    item = catalog.find("workflow", slug)
    if not isinstance(item, Workflow):
        return _unknown(slug, [w.slug for w in catalog.workflows])
    if phase_id is not None:
        return _phase_view(item, phase_id)
    fm = item.frontmatter
    extras = {
        k: v
        for k, v in (fm.model_extra or {}).items()
        if k not in WorkflowViewFull.model_fields
    }
    return WorkflowViewFull(
        slug=item.slug,
        name=fm.name,
        description=fm.description,
        version=fm.version,
        phases=[p.model_dump() for p in fm.phases],
        body=item.body,
        **extras,
    )


def get_checklist(
    catalog: Catalog, workflow_slug: str, phase_id: str
) -> ChecklistView | ErrorView:
    """Public entry for the ``agent_hq.get_checklist`` tool."""
    item = catalog.find("workflow", workflow_slug)
    if not isinstance(item, Workflow):
        return _unknown(workflow_slug, [w.slug for w in catalog.workflows])
    return _phase_view(item, phase_id)


def _phase_view(item: Workflow, phase_id: str) -> ChecklistView | ErrorView:
    phases = item.frontmatter.phases
    index = next((i for i, p in enumerate(phases) if p.id == phase_id), None)
    if index is None:
        known = [p.id for p in phases]
        return ErrorView(
            error=f"workflow '{item.slug}' has no phase '{phase_id}'", known_slugs=known
        )
    phase = phases[index]
    next_phase = phases[index + 1].id if index + 1 < len(phases) else None
    return ChecklistView(
        slug=item.slug,
        phase_id=phase.id,
        title=phase.display_title,
        checklist=list(phase.checklist),
        gate=phase.gate.model_dump(exclude_none=True),
        next_after_pass=next_phase,
        body_section=_body_section(item.body, phase),
    )


def _body_section(body: str, phase) -> str | None:
    """Extract the phase's markdown section (``### <id>``) from the workflow body."""
    marker = f"### {phase.id}"
    if marker not in body:
        return None
    start = body.index(marker) + len(marker)
    next_section = body.find("\n### ", start)
    section = body[start : next_section if next_section != -1 else len(body)]
    return section.strip() or None


def _unknown(slug: str, known: list[str]) -> ErrorView:
    log.info("get_workflow: unknown slug '%s'", slug)
    return ErrorView(error=f"no workflow with slug '{slug}'", known_slugs=known)
