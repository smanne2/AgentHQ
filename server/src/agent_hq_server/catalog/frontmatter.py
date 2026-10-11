"""Split and parse YAML frontmatter from markdown content files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from agent_hq_server.util.result import ContentError

FENCE = "---"
_CLOSERS = (FENCE, "...")


@dataclass(frozen=True)
class ParsedDoc:
    path: Path
    frontmatter: dict[str, object]
    body: str


def parse_markdown(path: Path) -> ParsedDoc:
    """Parse ``---`` fenced YAML frontmatter + markdown body.

    Tolerates a UTF-8 BOM and CRLF line endings; raises ContentError with a
    precise reason on anything malformed (the catalog turns that into an issue).
    """
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or _strip(lines[0]) != FENCE:
        raise ContentError(f"{path}: missing opening '---' frontmatter fence")

    closing: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if _strip(line) in _CLOSERS:
            closing = index
            break
    if closing is None:
        raise ContentError(f"{path}: missing closing '---' frontmatter fence")

    raw = "\n".join(lines[1:closing])
    data: object = yaml.safe_load(raw) if raw.strip() else {}
    if not isinstance(data, dict):
        raise ContentError(f"{path}: frontmatter must be a YAML mapping")
    body = "\n".join(lines[closing + 1 :]).lstrip("\n")
    return ParsedDoc(path=path, frontmatter=dict(data), body=body)


def parse_yaml_file(path: Path) -> dict[str, object]:
    """Parse a pure-YAML content file (profiles); must be a mapping at the top."""
    data: object = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ContentError(f"{path}: expected a YAML mapping")
    return dict(data)


def _strip(line: str) -> str:
    return line.strip()
