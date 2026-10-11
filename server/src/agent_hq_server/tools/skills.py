"""``agent_hq.list_skills`` / ``agent_hq.get_skill`` handlers.

``files`` is a sibling manifest (paths only): the server never executes skill
scripts — the agent runs them with its own tools.
"""

from __future__ import annotations

import logging

from agent_hq_server.catalog.catalog import Catalog, Skill
from agent_hq_server.schema import ErrorView, SkillSummary, SkillView

log = logging.getLogger(__name__)


def _skill_files(skill: Skill) -> list[str]:
    """Relative paths of every sibling file under the skill directory."""
    root = skill.path.parent
    files: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path != skill.path:
            files.append(str(path.relative_to(root)))
    return files


def list_skills(catalog: Catalog) -> list[SkillSummary]:
    """G5: slugs + one-liners; ``files`` carries the (small) sibling manifest."""
    return [
        SkillSummary(slug=s.slug, description=s.frontmatter.description, files=_skill_files(s))
        for s in catalog.skills
    ]


def get_skill(catalog: Catalog, slug: str) -> SkillView | ErrorView:
    """Full skill body + sibling manifest, or a typed error."""
    item = catalog.find("skill", slug)
    if not isinstance(item, Skill):
        return _unknown(slug, [s.slug for s in catalog.skills])
    fm = item.frontmatter
    extras = {k: v for k, v in (fm.model_extra or {}).items() if k not in SkillView.model_fields}
    return SkillView(
        slug=item.slug,
        name=fm.name,
        description=fm.description,
        files=_skill_files(item),
        body=item.body,
        **extras,
    )


def _unknown(slug: str, known: list[str]) -> ErrorView:
    log.info("get_skill: unknown slug '%s'", slug)
    return ErrorView(error=f"no skill with slug '{slug}'", known_slugs=known)
