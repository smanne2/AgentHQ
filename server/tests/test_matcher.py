"""Profile picking (pinned > auto > fallback) and instruction glob matching."""

from pathlib import Path

import pytest
import yaml
from agent_hq_server.catalog.catalog import load
from agent_hq_server.catalog.matcher import match_instructions, pick_profile

PROFILES_YAML = {
    "node-web": {
        "id": "node-web",
        "name": "Node Web",
        "description": "TypeScript/Node services",
        "matches": {
            "anyOf": [
                {"file": "package.json", "containsAny": ["express", "typescript"]},
            ]
        },
    },
    "python-oss": {
        "id": "python-oss",
        "name": "Python OSS",
        "description": "Python projects",
        "matches": {"anyOf": [{"file": "pyproject.toml"}]},
    },
    "default": {
        "id": "default",
        "name": "Default",
        "description": "Generic fallback",
    },
}


@pytest.fixture()
def catalog(tmp_path: Path):
    root = tmp_path / "content" / "profiles"
    root.mkdir(parents=True)
    for _, data in PROFILES_YAML.items():
        (root / f"{data['id']}.profile.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    return load(tmp_path / "content")


def test_pinned_profile_wins(catalog) -> None:
    item, source = pick_profile(catalog, pinned_id="python-oss")
    assert item.frontmatter.id == "python-oss"
    assert source == "pinned"


def test_auto_match_on_manifest_signals(catalog) -> None:
    item, source = pick_profile(
        catalog,
        signals={"package.json": '{"name": "svc", "dependencies": {"express": "4"}}'},
    )
    assert source == "auto"
    assert item.frontmatter.id == "node-web"


def test_auto_match_on_file_presence(catalog) -> None:
    item, source = pick_profile(catalog, signals={"pyproject.toml": "[project]"})
    assert source == "auto"
    assert item.frontmatter.id == "python-oss"


def test_unmatched_signals_fall_back_to_default(catalog) -> None:
    item, source = pick_profile(catalog, signals={"go.mod": "module x"})
    assert source == "fallback"
    assert item.frontmatter.id == "default"


def test_no_signals_fall_back_to_default(catalog) -> None:
    item, source = pick_profile(catalog)
    assert source == "fallback"
    assert item.frontmatter.id == "default"


def test_unknown_pin_degrades_to_fallback(catalog) -> None:
    item, source = pick_profile(catalog, pinned_id="nope", signals=None)
    assert source == "fallback"
    assert item.frontmatter.id == "default"


def test_no_profiles_raises(tmp_path: Path) -> None:
    empty = load(tmp_path / "content")
    with pytest.raises(LookupError):
        pick_profile(empty)


def test_instruction_matching_by_globs(tmp_path: Path) -> None:
    root = tmp_path / "content" / "instructions"
    root.mkdir(parents=True)
    (root / "global.instructions.md").write_text(
        "---\ndescription: always on\n---\nbody\n", encoding="utf-8"
    )
    (root / "ts.instructions.md").write_text(
        "---\ndescription: ts only\napplyTo: '**/*.ts'\n---\nbody\n", encoding="utf-8"
    )
    catalog = load(tmp_path / "content")

    ts_project = match_instructions(catalog.instructions, ["src/index.ts", "README.md"])
    assert {item.slug for item in ts_project} == {"global", "ts"}

    rust_project = match_instructions(catalog.instructions, ["src/main.rs"])
    assert {item.slug for item in rust_project} == {"global"}

    no_files = match_instructions(catalog.instructions, [])
    assert {item.slug for item in no_files} == {"global"}


def test_tag_filter(tmp_path: Path) -> None:
    root = tmp_path / "content" / "instructions"
    root.mkdir(parents=True)
    (root / "a.instructions.md").write_text(
        "---\ndescription: d\ntags: [typescript]\n---\nb\n", encoding="utf-8"
    )
    (root / "b.instructions.md").write_text("---\ndescription: d\n---\nb\n", encoding="utf-8")
    catalog = load(tmp_path / "content")

    tagged = match_instructions(catalog.instructions, ["x.ts"], tag="typescript")
    assert [item.slug for item in tagged] == ["a"]

    untagged = match_instructions(catalog.instructions, ["x.ts"], tag="python")
    assert untagged == []
