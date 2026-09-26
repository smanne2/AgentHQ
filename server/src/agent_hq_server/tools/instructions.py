"""``agent_hq.list_instructions`` / ``agent_hq.get_instruction`` handlers.

Conventions (``content/conventions/``) are instructions with a directory
marker (DD5): they share these tools, flagged by the ``convention`` field.
"""

from __future__ import annotations

import logging

from agent_hq_server.catalog.catalog import Catalog, Instruction
from agent_hq_server.schema import ErrorView, InstructionSummary, InstructionViewFull

log = logging.getLogger(__name__)

_CONVENTION_DIR = "conventions"


def list_instructions(
    catalog: Catalog,
    tag: str | None = None,
    convention: bool | None = None,
) -> list[InstructionSummary]:
    """G5: slugs + one-liners. ``convention`` filters to that directory."""
    selected = catalog.instructions
    if convention is not None:
        selected = [i for i in selected if _is_convention(i) == convention]
    if tag:
        selected = [i for i in selected if tag in (i.frontmatter.tags or [])]
    return [
        InstructionSummary(
            slug=i.slug, description=i.frontmatter.description, apply_to=i.frontmatter.apply_to
        )
        for i in selected
    ]


def get_instruction(catalog: Catalog, slug: str) -> InstructionViewFull | ErrorView:
    """Full instruction text, or a typed error listing known slugs."""
    item = catalog.find("instruction", slug)
    if not isinstance(item, Instruction):
        return _unknown(slug, [i.slug for i in catalog.instructions])
    fm = item.frontmatter
    extras = {
        k: v for k, v in (fm.model_extra or {}).items() if k not in InstructionViewFull.model_fields
    }
    return InstructionViewFull(
        slug=item.slug,
        description=fm.description,
        apply_to=fm.apply_to,
        tags=fm.tags,
        convention=_is_convention(item),
        body=item.body,
        **extras,
    )


def _is_convention(item: Instruction) -> bool:
    """Conventions live in ``content/conventions/`` (DD5) — same schema, own dir."""
    return _CONVENTION_DIR in item.path.parts


def _unknown(slug: str, known: list[str]) -> ErrorView:
    log.info("get_instruction: unknown slug '%s'", slug)
    return ErrorView(error=f"no instruction with slug '{slug}'", known_slugs=known)
