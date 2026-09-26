"""Frontmatter parsing: fences, YAML shapes, error handling."""

from pathlib import Path

import pytest
from agent_hq_server.catalog.frontmatter import parse_markdown, parse_yaml_file
from agent_hq_server.util.result import ContentError


def _write(tmp_path: Path, text: str, name: str = "doc.md") -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_parses_frontmatter_and_body(tmp_path) -> None:
    path = _write(
        tmp_path,
        "---\nname: Foo\ndescription: does things\n---\n# Body\n\nhello\n",
    )
    doc = parse_markdown(path)
    assert doc.frontmatter == {"name": "Foo", "description": "does things"}
    assert doc.body.startswith("# Body")
    assert not doc.body.startswith("\n")


def test_tolerates_bom_and_crlf(tmp_path) -> None:
    path = _write(tmp_path, "\ufeff---\r\ndescription: x\r\n---\r\nbody\r\n")
    doc = parse_markdown(path)
    assert doc.frontmatter == {"description": "x"}
    assert doc.body == "body"


def test_empty_frontmatter_is_allowed(tmp_path) -> None:
    doc = parse_markdown(_write(tmp_path, "---\n---\nbody\n"))
    assert doc.frontmatter == {}


def test_missing_opening_fence_raises(tmp_path) -> None:
    with pytest.raises(ContentError, match="opening"):
        parse_markdown(_write(tmp_path, "no fence here\n---\n"))


def test_missing_closing_fence_raises(tmp_path) -> None:
    with pytest.raises(ContentError, match="closing"):
        parse_markdown(_write(tmp_path, "---\nname: x\nno close\n"))


def test_non_mapping_frontmatter_raises(tmp_path) -> None:
    with pytest.raises(ContentError, match="mapping"):
        parse_markdown(_write(tmp_path, "---\n- a\n- b\n---\nbody\n"))


def test_dots_fence_closes(tmp_path) -> None:
    doc = parse_markdown(_write(tmp_path, "---\ndescription: x\n...\nbody\n"))
    assert doc.frontmatter == {"description": "x"}


def test_yaml_file_must_be_mapping(tmp_path) -> None:
    path = _write(tmp_path, "- a\n- b\n", "p.yaml")
    with pytest.raises(ContentError, match="mapping"):
        parse_yaml_file(path)


def test_yaml_file_parses(tmp_path) -> None:
    path = _write(tmp_path, "id: node-web\nname: Node\n", "p.yaml")
    assert parse_yaml_file(path) == {"id": "node-web", "name": "Node"}
