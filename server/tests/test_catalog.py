"""Catalog index: real awesome-copilot fixtures, issues, duplicates, digest."""

import shutil
import time
from pathlib import Path

from agent_hq_server.catalog.catalog import Instruction, Role, load

FIXTURES = Path(__file__).parent / "fixtures" / "content"


def test_fixture_tree_loads_with_zero_rework() -> None:
    """Real awesome-copilot files must import cleanly (DD4) — no issues."""
    catalog = load(FIXTURES)
    assert [role.slug for role in catalog.roles] == [
        "accessibility",
        "address-comments",
        "adr-generator",
    ]
    assert {item.slug for item in catalog.instructions} == {
        "a11y",
        "agent-safety",
        "astro",
    }
    assert {skill.slug for skill in catalog.skills} == {
        "acquire-codebase-knowledge",
        "code-review",
    }
    assert catalog.issues == []
    assert len(catalog.version) == 10


def test_astro_comma_globs_normalized() -> None:
    catalog = load(FIXTURES)
    astro = catalog.find("instruction", "astro")
    assert isinstance(astro, Instruction)
    assert astro.frontmatter.apply_to == [
        "**/*.astro",
        "**/*.ts",
        "**/*.js",
        "**/*.md",
        "**/*.mdx",
    ]


def test_role_extras_preserved() -> None:
    catalog = load(FIXTURES)
    accessibility = catalog.find("role", "accessibility")
    assert isinstance(accessibility, Role)
    assert accessibility.frontmatter.name == "Accessibility Expert"
    assert accessibility.frontmatter.model == "GPT-4.1"
    assert "search" in (accessibility.frontmatter.tools or [])


def test_digest_stable_and_sensitive(tmp_path) -> None:
    first = load(FIXTURES).version
    assert first == load(FIXTURES).version
    copy = tmp_path / "content"
    shutil.copytree(FIXTURES, copy)
    assert load(copy).version == first
    (copy / "agents" / "accessibility.agent.md").write_text(
        "---\nname: changed\ndescription: x\n---\nbody\n", encoding="utf-8"
    )
    assert load(copy).version != first


def test_malformed_file_becomes_issue_not_crash(tmp_path) -> None:
    root = tmp_path / "content"
    (root / "agents").mkdir(parents=True)
    (root / "agents" / "good.agent.md").write_text(
        "---\nname: Good\ndescription: fine\n---\nbody\n", encoding="utf-8"
    )
    (root / "agents" / "bad.agent.md").write_text(
        "---\nname: Broken\nunclosed fence\n", encoding="utf-8"
    )
    catalog = load(root)
    assert [role.slug for role in catalog.roles] == ["good"]
    assert len(catalog.issues) == 1
    assert "bad.agent.md" in catalog.issues[0].path


def test_duplicate_slug_across_directories_flagged(tmp_path) -> None:
    root = tmp_path / "content"
    for directory in ("instructions", "conventions"):
        (root / directory).mkdir(parents=True)
        (root / directory / "typescript.instructions.md").write_text(
            "---\ndescription: ts rules\napplyTo: '**/*.ts'\n---\nbody\n",
            encoding="utf-8",
        )
    catalog = load(root)
    assert len(catalog.instructions) == 1
    assert any("duplicate" in issue.message for issue in catalog.issues)


def test_missing_root_is_an_issue(tmp_path) -> None:
    catalog = load(tmp_path / "does-not-exist")
    assert catalog.version == "missing"
    assert any("does not exist" in issue.message for issue in catalog.issues)


def test_counts_helper(tmp_path) -> None:
    catalog = load(FIXTURES)
    assert catalog.counts() == {
        "role": 3,
        "instruction": 3,
        "skill": 2,
        "workflow": 1,
        "profile": 1,
    }


def test_fixture_tree_loads_fast() -> None:
    started = time.perf_counter()
    for _ in range(10):
        load(FIXTURES)
    average = (time.perf_counter() - started) / 10
    assert average < 0.5, f"catalog load too slow: {average * 1000:.1f} ms average"
