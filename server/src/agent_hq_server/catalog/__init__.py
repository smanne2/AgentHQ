"""Content engine: parse the content tree, index it, match it to projects."""

from agent_hq_server.catalog.bundle import assemble_bundle
from agent_hq_server.catalog.catalog import Catalog, Instruction, ProfileItem, Role, load
from agent_hq_server.catalog.detect import detect_stack, detect_stack_from_signals
from agent_hq_server.catalog.matcher import match_instructions, pick_profile

__all__ = [
    "Catalog",
    "Instruction",
    "ProfileItem",
    "Role",
    "assemble_bundle",
    "detect_stack",
    "detect_stack_from_signals",
    "load",
    "match_instructions",
    "pick_profile",
]
