"""Pydantic v2 models for every content kind + bootstrap bundle shapes."""

from agent_hq_server.schema.bundle import (
    Bundle,
    BundleProfile,
    InstructionSummary,
    InstructionView,
    PhaseView,
    RoleSummary,
    SkillSummary,
    WorkflowView,
)
from agent_hq_server.schema.common import ContentBase
from agent_hq_server.schema.instruction import InstructionFrontmatter
from agent_hq_server.schema.profile import Defaults, FileMatch, Matches, Profile
from agent_hq_server.schema.role import RoleFrontmatter
from agent_hq_server.schema.skill import SkillFrontmatter
from agent_hq_server.schema.view import (
    ChecklistView,
    ContentInfoView,
    Counts,
    ErrorView,
    InstructionViewFull,
    RoleView,
    SkillView,
    WorkflowSummary,
    WorkflowViewFull,
)
from agent_hq_server.schema.workflow import Gate, Phase, WorkflowFrontmatter

__all__ = [
    "Bundle",
    "BundleProfile",
    "ChecklistView",
    "ContentBase",
    "ContentInfoView",
    "Counts",
    "Defaults",
    "ErrorView",
    "FileMatch",
    "Gate",
    "InstructionFrontmatter",
    "InstructionSummary",
    "InstructionView",
    "InstructionViewFull",
    "Matches",
    "Phase",
    "PhaseView",
    "Profile",
    "RoleFrontmatter",
    "RoleSummary",
    "RoleView",
    "SkillFrontmatter",
    "SkillSummary",
    "SkillView",
    "WorkflowFrontmatter",
    "WorkflowSummary",
    "WorkflowView",
    "WorkflowViewFull",
]
