"""Phase 3: stack detection, profile→bundle assembly, and the bootstrap wiring.

Acceptance (plan.md Phase 3): different stacks → different bundles; pinned
profile overrides detection; fallback when undetectable.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from agent_hq_server.catalog.bundle import assemble_bundle
from agent_hq_server.catalog.catalog import Catalog, ProfileItem, load
from agent_hq_server.catalog.detect import detect_stack
from agent_hq_server.schema import Bundle, ErrorView
from agent_hq_server.tools.bootstrap import _project_file_patterns, bootstrap

FIXTURES = Path(__file__).parent / "fixtures" / "content"

# Full content tree for the bundle/bootstrap tests: 3 profiles + the real
# standard-feature workflow + one global instruction. Self-contained so the
# bundle assertions are stable regardless of content/ evolution.
PROFILES_YAML = {
    "node-web": {
        "id": "node-web",
        "name": "Node.js Web Service (TypeScript)",
        "description": "TypeScript/Node API or web service projects.",
        "matches": {"anyOf": [{"file": "package.json"}]},
        "stack": ["typescript", "node"],
        "defaults": {
            "workflow": "standard-feature",
            "roles": ["architect", "engineer", "code-reviewer", "test-engineer"],
            "instructions": ["agent-safety"],
            "skills": ["acquire-codebase-knowledge"],
        },
    },
    "python-oss": {
        "id": "python-oss",
        "name": "Python OSS Project",
        "description": "Python open source projects.",
        "matches": {"anyOf": [{"file": "pyproject.toml"}]},
        "stack": ["python"],
        "defaults": {
            "workflow": "standard-feature",
            "roles": [
                "architect",
                "engineer",
                "code-reviewer",
                "test-engineer",
                "docs-writer",
            ],
            "instructions": ["agent-safety"],
            "skills": ["acquire-codebase-knowledge"],
        },
    },
    "default": {
        "id": "default",
        "name": "Default",
        "description": "Generic fallback profile.",
        "matches": None,
        "stack": [],
        "defaults": {
            "workflow": "standard-feature",
            "roles": [],
            "instructions": ["agent-safety"],
            "skills": ["acquire-codebase-knowledge"],
        },
    },
}


def _write_profile(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


ROLE_MD = {
    "architect": "---\nname: Architect\ndescription: System design.\n---\nArchitect\n",
    "engineer": "---\nname: Engineer\ndescription: Implementation.\n---\nEngineer\n",
    "code-reviewer": "---\nname: Code Reviewer\ndescription: Reviews.\n---\nReviewer\n",
    "test-engineer": "---\nname: Test Engineer\ndescription: Tests.\n---\nTester\n",
    "docs-writer": "---\nname: Docs Writer\ndescription: Docs.\n---\nWriter\n",
}


def _node_project(tmp_path: Path) -> Path:
    project = tmp_path / "node-proj"
    (project / "src").mkdir(parents=True)
    (project / "package.json").write_text(
        json.dumps({"name": "svc", "devDependencies": {"typescript": "5"}}),
        encoding="utf-8",
    )
    (project / "src" / "index.ts").write_text("export {}\n", encoding="utf-8")
    return project


def _python_project(tmp_path: Path) -> Path:
    project = tmp_path / "py-proj"
    (project / "src").mkdir(parents=True)
    (project / "pyproject.toml").write_text("[project]\nname = 'svc'\n", encoding="utf-8")
    (project / "src" / "main.py").write_text("print('hi')\n", encoding="utf-8")
    return project


def _pin(project: Path, profile_id: str) -> None:
    (project / ".agent-hq").mkdir(parents=True, exist_ok=True)
    (project / ".agent-hq" / "profile.yaml").write_text(
        f"profile: {profile_id}\n", encoding="utf-8"
    )


def _assert_bundle(result: object) -> Bundle:
    assert isinstance(result, Bundle), f"expected Bundle, got {type(result).__name__}"
    return result


def _profile(catalog: Catalog, slug: str) -> ProfileItem:
    item = catalog.find("profile", slug)
    assert isinstance(item, ProfileItem), f"expected profile {slug}, got {type(item).__name__}"
    return item


@pytest.fixture()
def catalog(tmp_path: Path) -> Catalog:
    root = tmp_path / "content"
    for pid, data in PROFILES_YAML.items():
        _write_profile(root / "profiles" / f"{pid}.profile.yaml", data)
    # Reuse the real workflow (stable phase ids discover/design/…).
    (root / "workflows").mkdir(parents=True, exist_ok=True)
    for wf in (FIXTURES / "workflows").iterdir():
        if wf.is_file():
            (root / "workflows" / wf.name).write_bytes(wf.read_bytes())
    (root / "instructions").mkdir(parents=True, exist_ok=True)
    (root / "instructions" / "agent-safety.instructions.md").write_text(
        "---\ndescription: agent safety\n---\nBe safe\n", encoding="utf-8"
    )
    (root / "agents").mkdir(parents=True, exist_ok=True)
    for slug, text in ROLE_MD.items():
        (root / "agents" / f"{slug}.agent.md").write_text(text, encoding="utf-8")
    (root / "skills" / "acquire-codebase-knowledge").mkdir(parents=True, exist_ok=True)
    (root / "skills" / "acquire-codebase-knowledge" / "SKILL.md").write_text(
        "---\ndescription: Acquire knowledge\n---\nScan\n", encoding="utf-8"
    )
    return load(root)


def test_bootstrap_node_project_selects_node_web(catalog: Catalog, tmp_path: Path) -> None:
    result = _assert_bundle(bootstrap(catalog, _node_project(tmp_path)))
    assert result.profile.model_dump() == {
        "id": "node-web",
        "name": "Node.js Web Service (TypeScript)",
        "source": "auto",
    }
    assert result.workflow is not None and result.workflow.slug == "standard-feature"
    assert {r.slug for r in result.roles} == {
        "architect",
        "engineer",
        "code-reviewer",
        "test-engineer",
    }
    assert "Start phase 'discover'" in result.next_action


def test_bootstrap_python_project_selects_python_oss(catalog: Catalog, tmp_path: Path) -> None:
    result = _assert_bundle(bootstrap(catalog, _python_project(tmp_path)))
    assert result.profile.id == "python-oss"
    assert result.profile.source == "auto"
    assert "docs-writer" in {r.slug for r in result.roles}


def test_different_stacks_yield_different_bundles(catalog: Catalog, tmp_path: Path) -> None:
    node = _assert_bundle(bootstrap(catalog, _node_project(tmp_path)))
    python = _assert_bundle(bootstrap(catalog, _python_project(tmp_path)))
    assert node.profile.id == "node-web"
    assert python.profile.id == "python-oss"
    assert {r.slug for r in node.roles} != {r.slug for r in python.roles}


def test_bootstrap_undetectable_project_falls_back(catalog: Catalog, tmp_path: Path) -> None:
    project = tmp_path / "bare"
    project.mkdir()
    result = _assert_bundle(bootstrap(catalog, project))
    assert result.profile.id == "default"
    assert result.profile.source == "fallback"
    assert result.workflow is not None
    assert {i.slug for i in result.instructions} == {"agent-safety"}


def test_bootstrap_pinned_profile_overrides_detection(catalog: Catalog, tmp_path: Path) -> None:
    project = _node_project(tmp_path)
    _pin(project, "python-oss")
    result = _assert_bundle(bootstrap(catalog, project))
    assert result.profile.id == "python-oss"
    assert result.profile.source == "pinned"


def test_bootstrap_explicit_pin_beats_file_pin(catalog: Catalog, tmp_path: Path) -> None:
    project = _node_project(tmp_path)
    _pin(project, "python-oss")
    result = _assert_bundle(bootstrap(catalog, project, pinned_profile="node-web"))
    assert result.profile.id == "node-web"
    assert result.profile.source == "pinned"


def test_glob_instructions_require_project_files(tmp_path: Path) -> None:
    """A profile instruction with applyTo is inlined only when a project file matches."""
    root = tmp_path / "content"
    _write_profile(
        root / "profiles" / "node-web.profile.yaml",
        {
            "id": "node-web",
            "defaults": {"instructions": ["ts"]},
            "matches": {"anyOf": [{"file": "package.json"}]},
        },
    )
    (root / "instructions").mkdir(parents=True, exist_ok=True)
    (root / "instructions" / "ts.instructions.md").write_text(
        "---\ndescription: ts only\napplyTo: '**/*.ts'\n---\nbody\n", encoding="utf-8"
    )
    test_catalog = load(root)
    profile = _profile(test_catalog, "node-web")

    warnings: list[str] = []
    with_files = assemble_bundle(test_catalog, profile, "auto", ["src/index.ts"], warnings)
    without_files = assemble_bundle(test_catalog, profile, "auto", ["README.md"], warnings)
    assert "ts" in {i.slug for i in with_files.instructions}
    assert "ts" not in {i.slug for i in without_files.instructions}
    assert any("ts" in w and "no project file matched" in w for w in warnings)


def test_assemble_bundle_warns_on_unknown_slugs(tmp_path: Path) -> None:
    root = tmp_path / "content"
    (root / "workflows").mkdir(parents=True, exist_ok=True)
    (root / "workflows" / "wf.workflow.md").write_text(
        "---\nname: WF\ndescription: d\nphases:\n  - id: p1\ntitle: P\n---\nbody\n",
        encoding="utf-8",
    )
    _write_profile(
        root / "profiles" / "bad.profile.yaml",
        {
            "id": "bad",
            "defaults": {
                "workflow": "nope",
                "roles": ["ghost"],
                "skills": ["phantom"],
            },
        },
    )
    test_catalog = load(root)
    profile = _profile(test_catalog, "bad")

    warnings: list[str] = []
    bundle = assemble_bundle(test_catalog, profile, "fallback", [], warnings)
    assert bundle.workflow is None
    assert bundle.roles == []
    assert "unknown workflow 'nope'" in " ".join(warnings)
    assert "unknown role 'ghost'" in " ".join(warnings)
    assert "unknown skill 'phantom'" in " ".join(warnings)


def test_detect_stack_reads_manifests(tmp_path: Path) -> None:
    node = _node_project(tmp_path)
    assert "package.json" in detect_stack(node)

    python = _python_project(tmp_path)
    assert "pyproject.toml" in detect_stack(python)

    bare = tmp_path / "empty"
    bare.mkdir()
    assert detect_stack(bare) == {}


def test_project_file_patterns_prunes_vendor_dirs(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    (project / "node_modules" / "pkg").mkdir(parents=True)
    (project / "src").mkdir()
    (project / ".git").mkdir()
    (project / "src" / "index.ts").write_text("x", encoding="utf-8")
    (project / "node_modules" / "pkg" / "index.js").write_text("x", encoding="utf-8")
    (project / ".git" / "HEAD").write_text("x", encoding="utf-8")

    patterns = _project_file_patterns(project)
    assert "src/index.ts" in patterns
    assert not any("node_modules" in p or ".git" in p for p in patterns)


def test_project_file_patterns_missing_dir(tmp_path: Path) -> None:
    assert _project_file_patterns(tmp_path / "nope") == []


def test_bootstrap_error_view_when_no_profiles(tmp_path: Path) -> None:
    empty_catalog = load(tmp_path / "content")  # directory does not exist
    project = tmp_path / "proj"
    project.mkdir()
    result = bootstrap(empty_catalog, project)
    assert isinstance(result, ErrorView)
    assert "profile selection failed" in result.error
