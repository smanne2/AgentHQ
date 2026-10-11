"""Slug and digest utilities."""

from pathlib import Path

from agent_hq_server.util.digest import content_digest
from agent_hq_server.util.slug import slug_from_dir, slug_from_filename


def test_slug_from_filename_strips_kind_suffix() -> None:
    assert slug_from_filename(Path("agents/accessibility.agent.md"), (".agent.md",)) == (
        "accessibility"
    )
    assert slug_from_filename(Path("agents/my.cool.role.agent.md"), (".agent.md",)) == (
        "my-cool-role"
    )


def test_slug_from_filename_explicit_suffix() -> None:
    assert (
        slug_from_filename(Path("profiles/node-web.profile.yaml"), (".profile.yaml",)) == "node-web"
    )


def test_slug_from_dir_uses_skill_directory() -> None:
    path = Path("skills/acquire-codebase-knowledge/SKILL.md")
    assert slug_from_dir(path) == "acquire-codebase-knowledge"


def test_slugify_handles_garbage() -> None:
    assert slug_from_filename(Path("agents/---.agent.md"), (".agent.md",)) == "unnamed"


def test_digest_changes_with_content(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("one", encoding="utf-8")
    first = content_digest(tmp_path)
    (tmp_path / "a.md").write_text("two", encoding="utf-8")
    assert content_digest(tmp_path) != first
    (tmp_path / "a.md").write_text("one", encoding="utf-8")
    assert content_digest(tmp_path) == first


def test_digest_missing_dir() -> None:
    assert content_digest(Path("/nonexistent/agent-hq-content")) == "missing"
