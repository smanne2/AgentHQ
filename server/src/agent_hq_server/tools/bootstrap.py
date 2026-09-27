"""``agent_hq.bootstrap`` — the session-start handshake (technical.md §3.1).

Assembly pipeline: pinned profile file → profile pick → bundle (workflow with
phases/checklists/gates, inlined instruction bodies, role roster, skills).
Phase 3 adds ``catalog/detect.py`` + ``catalog/bundle.py``; this module keeps
the same contract so the wiring is a swap, not a rewrite.
"""

from __future__ import annotations

import logging
from pathlib import Path

from agent_hq_server.catalog.catalog import Catalog, Instruction, Role
from agent_hq_server.catalog.matcher import pick_profile
from agent_hq_server.catalog.pin import read_pin_file
from agent_hq_server.schema import (
    Bundle,
    BundleProfile,
    ErrorView,
    InstructionView,
    PhaseView,
    RoleSummary,
    SkillSummary,
    WorkflowView,
)
from agent_hq_server.tools.skills import _skill_files

log = logging.getLogger(__name__)


def bootstrap(
    catalog: Catalog,
    project_path: Path,
    pinned_profile: str | None = None,
) -> Bundle | ErrorView:
    """Resolve the project's onboarding bundle.

    ``pinned_profile`` from an explicit argument wins; otherwise the project's
    ``.agent-hq/profile.yaml`` is consulted (technical.md §4.5 order).
    """
    file_pin, pin_warning = read_pin_file(project_path)
    effective_pin = pinned_profile or file_pin

    try:
        profile, source = pick_profile(catalog, pinned_id=effective_pin)
    except LookupError as exc:
        return ErrorView(
            error=f"profile selection failed: {exc}; add a profiles/ file to the content tree"
        )

    warnings = [pin_warning] if pin_warning else []
    defaults = profile.frontmatter.defaults

    workflow = _resolve_workflow(catalog, defaults.workflow, warnings)
    instructions = _resolve_instructions(catalog, defaults.instructions, warnings)
    roles = _resolve_roles(catalog, defaults.roles, warnings)
    skills = _resolve_skills(catalog, defaults.skills, warnings)

    first_phase = workflow.phases[0] if workflow and workflow.phases else None
    next_action = (
        f"Start phase '{first_phase.id}' ({first_phase.title}) of workflow "
        f"'{workflow.slug}': complete its checklist, then call agent_hq.report_progress."
        if first_phase and workflow is not None
        else "No workflow selected — ask the user which process to follow."
    )

    kwargs: dict[str, object] = {}
    if warnings:
        kwargs["warnings"] = warnings
    return Bundle(
        content_version=catalog.version,
        profile=BundleProfile(
            id=profile.frontmatter.id, name=profile.frontmatter.name, source=source
        ),
        workflow=workflow,
        instructions=instructions,
        roles=roles,
        skills=skills,
        next_action=next_action,
        **kwargs,
    )


def _resolve_workflow(
    catalog: Catalog, slug: str | None, warnings: list[str]
) -> WorkflowView | None:
    if not slug:
        return None
    for item in catalog.workflows:
        if item.slug != slug:
            continue
        fm = item.frontmatter
        return WorkflowView(
            slug=item.slug,
            name=fm.name,
            description=fm.description,
            phases=[
                PhaseView(
                    id=p.id,
                    title=p.display_title,
                    checklist=list(p.checklist),
                    gate=p.gate,
                )
                for p in fm.phases
            ],
        )
    warnings.append(f"profile references unknown workflow '{slug}'")
    return None


def _resolve_instructions(
    catalog: Catalog, slugs: list[str], warnings: list[str]
) -> list[InstructionView]:
    picked: dict[str, InstructionView] = {}

    def _add(item: Instruction) -> None:
        if item.slug in picked:
            return
        picked[item.slug] = InstructionView(
            slug=item.slug, description=item.frontmatter.description, body=item.body
        )

    by_slug = {item.slug: item for item in catalog.instructions}
    for slug in slugs:
        item = by_slug.get(slug)
        if item is None:
            warnings.append(f"profile references unknown instruction '{slug}'")
            continue
        _add(item)
    for item in catalog.instructions:  # global rules (no applyTo) always apply
        if item.frontmatter.apply_to is None:
            _add(item)
    return list(picked.values())


def _role_summary(role: Role) -> RoleSummary:
    return RoleSummary(
        slug=role.slug,
        name=role.frontmatter.name,
        description=role.frontmatter.description,
    )


def _resolve_roles(catalog: Catalog, slugs: list[str], warnings: list[str]) -> list[RoleSummary]:
    if not slugs:
        return [_role_summary(r) for r in catalog.roles]
    by_slug = {item.slug: item for item in catalog.roles}
    picked = [_role_summary(by_slug[slug]) for slug in slugs if (by_slug.get(slug)) is not None]
    unknown = [s for s in slugs if s not in by_slug]
    warnings.extend(f"profile references unknown role '{s}'" for s in unknown)
    return picked


def _resolve_skills(catalog: Catalog, slugs: list[str], warnings: list[str]) -> list[SkillSummary]:
    by_slug = {item.slug: item for item in catalog.skills}
    picked = [
        SkillSummary(slug=s.slug, description=s.frontmatter.description, files=_skill_files(s))
        for slug in slugs
        if (s := by_slug.get(slug)) is not None
    ]
    unknown = [s for s in slugs if s not in by_slug]
    warnings.extend(f"profile references unknown skill '{s}'" for s in unknown)
    return picked
