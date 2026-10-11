"""``agent_hq.list_roles`` / ``agent_hq.get_role`` handlers."""

from __future__ import annotations

import logging

from agent_hq_server.catalog.catalog import Catalog, Role
from agent_hq_server.schema import ErrorView, RoleSummary, RoleView

log = logging.getLogger(__name__)


def list_roles(catalog: Catalog, tag: str | None = None) -> list[RoleSummary]:
    """Roster (G5: slugs + one-liners only; full text via ``get_role``)."""
    selected = catalog.roles
    if tag:
        selected = [r for r in selected if tag in (r.frontmatter.tags or [])]
    return [
        RoleSummary(slug=r.slug, name=r.frontmatter.name, description=r.frontmatter.description)
        for r in selected
    ]


def get_role(catalog: Catalog, slug: str) -> RoleView | ErrorView:
    """Full role (persona prompt body + passthrough fields), or a typed error."""
    item = catalog.find("role", slug)
    if not isinstance(item, Role):
        return _unknown(slug, "role", [r.slug for r in catalog.roles])
    fm = item.frontmatter
    extras = {k: v for k, v in (fm.model_extra or {}).items() if k not in RoleView.model_fields}
    return RoleView(
        slug=item.slug,
        name=fm.name,
        description=fm.description,
        model=fm.model,
        tools=fm.tools,
        tags=fm.tags,
        body=item.body,
        **extras,
    )


def _unknown(slug: str, kind: str, known: list[str]) -> ErrorView:
    log.info("get_%s: unknown slug '%s'", kind, slug)
    return ErrorView(error=f"no {kind} with slug '{slug}'", known_slugs=known)
