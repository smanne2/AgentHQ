"""Onboarding bundle assembly.

Builds the bootstrap response from a selected profile and the catalog
(technical.md §4.5). Instructions are inlined in full (needed immediately);
roles and skills travel as summaries (G5).
"""

from __future__ import annotations

from collections.abc import Sequence

from agent_hq_server.catalog.catalog import (
    Catalog,
    Instruction,
    ProfileItem,
    Role,
    Skill,
    Workflow,
)
from agent_hq_server.catalog.matcher import ProfileSource, match_instructions
from agent_hq_server.schema import (
    Bundle,
    BundleProfile,
    InstructionView,
    PhaseView,
    RoleSummary,
    SkillSummary,
    WorkflowView,
)


def assemble_bundle(
    catalog: Catalog,
    profile: ProfileItem,
    source: ProfileSource,
    file_patterns: Sequence[str],
    warnings: list[str],
) -> Bundle:
    """Assemble the onboarding bundle for a selected profile.

    ``source`` is how the profile was chosen (pinned/auto/fallback).
    ``file_patterns`` are the project's relative file paths, used to evaluate
    the ``applyTo`` globs of profile-requested instructions. Global rules
    (no ``applyTo``) are always inlined.
    """
    defaults = profile.frontmatter.defaults

    workflow = _resolve_workflow(catalog, defaults.workflow, warnings)
    instructions = _resolve_instructions(
        catalog, defaults.instructions, file_patterns, warnings
    )
    roles = _resolve_roles(catalog, defaults.roles, warnings)
    skills = _resolve_skills(catalog, defaults.skills, warnings)

    first_phase = workflow.phases[0] if workflow and workflow.phases else None
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
            source=source,
        ),
        workflow=workflow,
        instructions=instructions,
        roles=roles,
        skills=skills,
        next_action=next_action,
    )


def _resolve_workflow(
    catalog: Catalog, slug: str | None, warnings: list[str]
) -> WorkflowView | None:
    if not slug:
        return None
    found = catalog.find("workflow", slug)
    if not isinstance(found, Workflow):
        warnings.append(f"profile references unknown workflow '{slug}'")
        return None
    fm = found.frontmatter
    return WorkflowView(
        slug=found.slug,
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


def _resolve_instructions(
    catalog: Catalog,
    slugs: list[str],
    file_patterns: Sequence[str],
    warnings: list[str],
) -> list[InstructionView]:
    by_slug = {item.slug: item for item in catalog.instructions}
    picked: dict[str, InstructionView] = {}

    # Profile-requested instructions: slug must exist, and any applyTo glob
    # must match at least one project file.
    for slug in slugs:
        item = by_slug.get(slug)
        if item is None:
            warnings.append(f"profile references unknown instruction '{slug}'")
            continue
        if item.frontmatter.apply_to and item.slug not in (
            m.slug for m in match_instructions([item], list(file_patterns))
        ):
            warnings.append(
                f"instruction '{slug}' applies to {_glob_of(item)} — no project file matched"
            )
            continue
        _add(picked, item)

    # Global rules (no applyTo) always apply, whatever the profile lists.
    for item in catalog.instructions:
        if item.frontmatter.apply_to is None:
            _add(picked, item)
    return list(picked.values())


def _add(picked: dict[str, InstructionView], item: Instruction) -> None:
    if item.slug not in picked:
        picked[item.slug] = InstructionView(
            slug=item.slug, description=item.frontmatter.description, body=item.body
        )


def _glob_of(item: Instruction) -> str:
    return ", ".join(item.frontmatter.apply_to or [])


def _role_summary(role: Role) -> RoleSummary:
    return RoleSummary(
        slug=role.slug,
        name=role.frontmatter.name,
        description=role.frontmatter.description,
    )


def _resolve_roles(
    catalog: Catalog, slugs: list[str], warnings: list[str]
) -> list[RoleSummary]:
    if not slugs:
        return [_role_summary(r) for r in catalog.roles]
    by_slug = {item.slug: item for item in catalog.roles}
    picked = [
        _role_summary(by_slug[slug])
        for slug in slugs
        if (by_slug.get(slug)) is not None
    ]
    unknown = [s for s in slugs if s not in by_slug]
    warnings.extend(f"profile references unknown role '{s}'" for s in unknown)
    return picked


def _resolve_skills(
    catalog: Catalog, slugs: list[str], warnings: list[str]
) -> list[SkillSummary]:
    by_slug = {item.slug: item for item in catalog.skills}
    picked = [
        SkillSummary(
            slug=s.slug, description=s.frontmatter.description, files=_skill_files(s)
        )
        for slug in slugs
        if (s := by_slug.get(slug)) is not None
    ]
    unknown = [s for s in slugs if s not in by_slug]
    warnings.extend(f"profile references unknown skill '{s}'" for s in unknown)
    return picked


def _skill_files(skill: Skill) -> list[str]:
    """Relative paths of every sibling file under the skill directory."""
    root = skill.path.parent
    return [
        str(path.relative_to(root))
        for path in sorted(root.rglob("*"))
        if path.is_file() and path != skill.path
    ]
