"""Build and query the in-memory content index over a ``content/`` tree.

Layout contract (kind by path):
    agents/*.agent.md            -> role
    instructions/**.instructions.md, conventions/**.instructions.md -> instruction
    skills/<name>/SKILL.md       -> skill
    workflows/*.workflow.md      -> workflow
    profiles/*.profile.yaml      -> profile

``load`` never raises for bad content: every problem becomes an Issue so one
malformed file can't break the index (technical.md R3).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from agent_hq_server.catalog import frontmatter as fm
from agent_hq_server.schema import (
    InstructionFrontmatter,
    Profile,
    RoleFrontmatter,
    SkillFrontmatter,
    WorkflowFrontmatter,
)
from agent_hq_server.util.digest import content_digest
from agent_hq_server.util.result import Issue
from agent_hq_server.util.slug import slug_from_dir, slug_from_filename

Kind = str  # "role" | "instruction" | "skill" | "workflow" | "profile"

_KIND_SUFFIXES = {
    "role": (".agent.md",),
    "instruction": (".instructions.md",),
    "skill": ("SKILL.md",),
    "workflow": (".workflow.md",),
    "profile": (".profile.yaml",),
}


@dataclass(frozen=True)
class Role:
    slug: str
    path: Path
    frontmatter: RoleFrontmatter
    body: str


@dataclass(frozen=True)
class Instruction:
    slug: str
    path: Path
    frontmatter: InstructionFrontmatter
    body: str


@dataclass(frozen=True)
class Skill:
    slug: str
    path: Path
    frontmatter: SkillFrontmatter
    body: str


@dataclass(frozen=True)
class Workflow:
    slug: str
    path: Path
    frontmatter: WorkflowFrontmatter
    body: str


@dataclass(frozen=True)
class ProfileItem:
    slug: str
    path: Path
    frontmatter: Profile  # pure YAML — no markdown body


@dataclass
class Catalog:
    root: Path
    version: str
    roles: list[Role] = field(default_factory=list)
    instructions: list[Instruction] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)
    workflows: list[Workflow] = field(default_factory=list)
    profiles: list[ProfileItem] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        return {
            "role": len(self.roles),
            "instruction": len(self.instructions),
            "skill": len(self.skills),
            "workflow": len(self.workflows),
            "profile": len(self.profiles),
        }

    def find(
        self, kind: Kind, slug: str
    ) -> Role | Instruction | Skill | Workflow | ProfileItem | None:
        items = {
            "role": self.roles,
            "instruction": self.instructions,
            "skill": self.skills,
            "workflow": self.workflows,
            "profile": self.profiles,
        }[kind]
        for item in items:
            if item.slug == slug:
                return item
        return None


def load(root: Path) -> Catalog:
    """Index the content tree; collect Issues instead of raising."""
    catalog = Catalog(
        root=root,
        version=content_digest(root) if root.is_dir() else "missing",
    )
    if not root.is_dir():
        catalog.issues.append(Issue(str(root), "content directory does not exist"))
        return catalog

    seen: dict[Kind, set[str]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        kind = _kind_for(rel)
        if kind is None:
            continue  # not a content file (READMEs, assets, …)
        try:
            item = _build_item(kind, path)
        except (fm.ContentError, ValidationError) as exc:
            catalog.issues.append(Issue(str(rel), _flatten(exc)))
            continue
        if item.slug in seen.setdefault(kind, set()):
            catalog.issues.append(Issue(str(rel), f"duplicate {kind} slug '{item.slug}'"))
            continue
        seen[kind].add(item.slug)
        _append(catalog, kind, item)
    return catalog


def _kind_for(rel: Path) -> Kind | None:
    parts = rel.parts
    if len(parts) == 2 and parts[0] == "agents" and parts[1].endswith(".agent.md"):
        return "role"
    if (
        len(parts) >= 2
        and parts[0] in ("instructions", "conventions")
        and parts[-1].endswith(".instructions.md")
    ):
        return "instruction"
    if len(parts) == 3 and parts[0] == "skills" and parts[-1] == "SKILL.md":
        return "skill"
    if len(parts) == 2 and parts[0] == "workflows" and parts[1].endswith(".workflow.md"):
        return "workflow"
    if len(parts) == 2 and parts[0] == "profiles" and parts[1].endswith(".profile.yaml"):
        return "profile"
    return None


def _build_item(kind: Kind, path: Path) -> Role | Instruction | Skill | Workflow | ProfileItem:
    if kind == "profile":
        data = fm.parse_yaml_file(path)
        frontmatter = Profile.model_validate(data)
        slug = slug_from_filename(path, _KIND_SUFFIXES["profile"])
        return ProfileItem(slug=slug, path=path, frontmatter=frontmatter)

    doc = fm.parse_markdown(path)
    if kind == "role":
        frontmatter = RoleFrontmatter.model_validate(doc.frontmatter)
        slug = slug_from_filename(path, _KIND_SUFFIXES["role"])
        return Role(slug=slug, path=path, frontmatter=frontmatter, body=doc.body)
    if kind == "instruction":
        frontmatter = InstructionFrontmatter.model_validate(doc.frontmatter)
        slug = slug_from_filename(path, _KIND_SUFFIXES["instruction"])
        return Instruction(slug=slug, path=path, frontmatter=frontmatter, body=doc.body)
    if kind == "skill":
        frontmatter = SkillFrontmatter.model_validate(doc.frontmatter)
        return Skill(slug=slug_from_dir(path), path=path, frontmatter=frontmatter, body=doc.body)
    frontmatter = WorkflowFrontmatter.model_validate(doc.frontmatter)
    slug = slug_from_filename(path, _KIND_SUFFIXES["workflow"])
    return Workflow(slug=slug, path=path, frontmatter=frontmatter, body=doc.body)


def _append(
    catalog: Catalog,
    kind: Kind,
    item: Role | Instruction | Skill | Workflow | ProfileItem,
) -> None:
    if kind == "role":
        catalog.roles.append(item)  # type: ignore[arg-type]
    elif kind == "instruction":
        catalog.instructions.append(item)  # type: ignore[arg-type]
    elif kind == "skill":
        catalog.skills.append(item)  # type: ignore[arg-type]
    elif kind == "workflow":
        catalog.workflows.append(item)  # type: ignore[arg-type]
    else:
        catalog.profiles.append(item)  # type: ignore[arg-type]


def _flatten(exc: Exception) -> str:
    """One-line message from a (possibly multi-error) pydantic ValidationError."""
    if isinstance(exc, ValidationError):
        first = exc.errors()[0]
        return f"invalid frontmatter: {first['msg']} ({first['loc']})"
    return str(exc)
