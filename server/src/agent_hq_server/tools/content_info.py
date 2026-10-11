"""``agent_hq.content_info`` — staleness detection + content tree overview."""

from __future__ import annotations

from agent_hq_server.catalog.catalog import Catalog
from agent_hq_server.schema import ContentInfoView, Counts


def content_info(catalog: Catalog) -> ContentInfoView:
    """Version digest + per-kind counts + profile ids."""
    counts = catalog.counts()
    return ContentInfoView(
        content_version=catalog.version,
        counts=Counts(
            roles=counts["role"],
            instructions=counts["instruction"],
            skills=counts["skill"],
            workflows=counts["workflow"],
            profiles=counts["profile"],
        ),
        profile_ids=[p.frontmatter.id for p in catalog.profiles],
        content_root=str(catalog.root),
    )
