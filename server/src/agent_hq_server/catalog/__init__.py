"""Content engine: parse the content tree, index it, match it to projects."""

from agent_hq_server.catalog.catalog import Catalog, Instruction, Role, load, ProfileItem
from agent_hq_server.catalog.matcher import match_instructions, pick_profile
from agent_hq_server.catalog.detect import detect_stack, detect_stack_from_signals
from agent_hq_server.catalog.bundle import assemble_bundle

__all__ = [
    "Catalog",
    "Instruction",
    "Role",
    "load",
    "ProfileItem",
    "match_instructions",
    "pick_profile",
    "detect_stack",
    "detect_stack_from_signals",
    "assemble_bundle",
]
