"""Onboarding bundle assembly.

Builds the bootstrap response from a profile and catalog.
"""

from __future__ import annotations

from pathlib import Path

from agent_hq_server.catalog.catalog import Catalog, ProfileItem, Skill
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


def assemble_bundle(
    catalog: Catalog,
    profile: ProfileItem,
    project_path: Path,
) -> Bundle | ErrorView:
    """Assemble an onboarding bundle from a profile and catalog.

    The bundle contains workflow, instructions, roles, and skills needed
    for the project. Instructions are included in full (needed immediately),
    while roles and skills are returned as summaries (lightweight).
    """
    defaults = profile.frontmatter.defaults

    workflow = _resolve_workflow(catalog, defaults.workflow)
    instructions = _resolve_instructions(catalog, defaults.instructions)
    roles = _resolve_roles(catalog, defaults.roles)
    skills = _resolve_skills(catalog, defaults.skills)

    first_phase = workflow.phases[0] if workflow and workflow.phases else None
    next_action = ""
    if first_phase and workflow:
        next_action = (
            f"Start phase '{first_phase.id}' ({first_phase.title}) of workflow "
            f"'{workflow.slug}': complete its checklist, then call agent_hq.report_progress."
        )
    else:
        next_action = "No workflow selected — ask the user which process to follow."

    return Bundle(
        content_version=catalog.version,
        profile=BundleProfile(
            id=profile.frontmatter.id,
            name=profile.frontmatter.name,
            source="pinned",  # Caller should set this based on how profile was selected
        ),
        workflow=workflow,
        instructions=instructions,
        roles=roles,
        skills=skills,
        next_action=next_action,
    )


def _resolve_workflow(catalog: Catalog, slug: str | None) -> WorkflowView | None:
    """Resolve a workflow by slug."""
    if not slug:
        return None

    for item in catalog.workflows:
        if item.slug == slug:
            fm = item.frontmatter
            return WorkflowView(
                slug=item.slug,
                name=fm.name,
                description=fm.description,
                phases=[
                    PhaseView(
                        id=p.id,
                        title=p.display_title,
                        checklist=list(p.checklist) if p.checklist else [],
                        gate=p.gate,
                    )
                    for p in fm.phases or []
                ],
            )
    return None


def _resolve_instructions(catalog: Catalog, slugs: list[str] | None) -> list[InstructionView]:
    """Resolve instructions by slug, including global instructions."""
    picked: dict[str, InstructionView] = {}

    # First add all global instructions (no applyTo)
    for item in catalog.instructions:
        if item.frontmatter.apply_to is None:
            picked[item.slug] = InstructionView(
                slug=item.slug,
                description=item.frontmatter.description,
                body=item.body,
            )

    # Then add requested instructions
    if slugs:
        for slug in slugs:
            for item in catalog.instructions:
                if item.slug == slug:
                    picked[item.slug] = InstructionView(
                        slug=item.slug,
                        description=item.frontmatter.description,
                        body=item.body,
                    )
                    break

    return list(picked.values())


def _resolve_roles(catalog: Catalog, slugs: list[str] | None) -> list[RoleSummary]:
    """Resolve roles by slug, or all roles if no slugs specified."""
    if not slugs:
        return [
            RoleSummary(
                slug=r.slug,
                name=r.frontmatter.name,
                description=r.frontmatter.description,
            )
            for r in catalog.roles
        ]

    picked: list[RoleSummary] = []
    for slug in slugs:
        for item in catalog.roles:
            if item.slug == slug:
                picked.append(
                    RoleSummary(
                        slug=item.slug,
                        name=item.frontmatter.name,
                        description=item.frontmatter.description,
                    )
                )
                break
    return picked


def _resolve_skills(catalog: Catalog, slugs: list[str] | None) -> list[SkillSummary]:
    """Resolve skills by slug, or all skills if no slugs specified."""
    if not slugs:
        return [
            SkillSummary(
                slug=s.slug,
                description=s.frontmatter.description,
                files=_get_skill_files(s),
            )
            for s in catalog.skills
        ]

    picked: list[SkillSummary] = []
    for slug in slugs:
        for item in catalog.skills:
            if item.slug == slug:
                picked.append(
                    SkillSummary(
                        slug=item.slug,
                        description=item.frontmatter.description,
                        files=_get_skill_files(item),
                    )
                )
                break
    return picked


def _get_skill_files(skill: Skill) -> list[str]:
    """Get file manifest for a skill."""
    files: list[str] = []
    skill_dir = skill.path.parent

    # List sibling files (scripts/, references/, etc.)
    if skill_dir.is_dir():
        for child in sorted(skill_dir.iterdir()):
            if child.is_file():
                files.append(child.name)

    return files
