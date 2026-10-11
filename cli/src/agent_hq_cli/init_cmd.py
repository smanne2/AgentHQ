"""`agent-hq init <dir>` — scaffold a new project for Agent HQ governance.

Writes the bootstrap stub (AGENTS.md), the client server config (mcp.json), and
the editable profile pin (.agent-hq/profile.yaml). Existing files are never
overwritten; they are reported so the user can reconcile.
"""

from __future__ import annotations

import json
from pathlib import Path

from agent_hq_cli.config import content_root, repo_root, templates_root

_PLACEHOLDER_MAP = {
    "__PROJECT_PATH__": "project_path",
    "__STACK__": "stack",
    "__PROFILE__": "profile",
    "__AGENT_HQ_ROOT__": "agent_hq_root",
    "__AGENT_HQ_CONTENT__": "content_path",
}


def _render(text: str, mapping: dict[str, str]) -> str:
    for token, value in mapping.items():
        text = text.replace(token, value)
    return text


def _write(path: Path, content: str, overwrite: bool) -> str:
    if path.exists() and not overwrite:
        return f"skipped (exists): {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"wrote: {path}"


def _detect(project: Path) -> tuple[str, str]:
    """Best-effort (stack, profile_id) for the project, via the server's matcher."""
    try:
        from agent_hq_server.catalog.catalog import load
        from agent_hq_server.catalog.detect import detect_stack
        from agent_hq_server.catalog.matcher import pick_profile

        from agent_hq_cli.config import content_root

        catalog = load(content_root())
        item, _source = pick_profile(catalog, signals=detect_stack(project))
        stack = item.frontmatter.stack[0] if item.frontmatter.stack else "unknown"
        return stack, item.frontmatter.id
    except Exception:
        return "unknown", "default"


def init_project(target: Path, profile: str, stack: str, overwrite: bool) -> list[str]:
    """Write the three artifacts into `target`; returns human-readable report lines."""
    values = {
        "project_path": str(target.resolve()),
        "stack": stack,
        "profile": profile,
        "agent_hq_root": str(repo_root()),
        "content_path": str(content_root()),
    }
    placeholders = {token: values[key] for token, key in _PLACEHOLDER_MAP.items()}
    templates = templates_root()
    report: list[str] = []

    agents_md = _render((templates / "AGENTS.md").read_text(encoding="utf-8"), placeholders)
    report.append(_write(target / "AGENTS.md", agents_md, overwrite))

    mcp_cfg = json.loads((templates / "mcp.json").read_text(encoding="utf-8"))
    mcp_cfg["mcpServers"]["agent-hq"]["args"] = [
        "run",
        "--project",
        values["agent_hq_root"],
        "agent-hq-server",
    ]
    mcp_cfg["mcpServers"]["agent-hq"]["env"]["AGENT_HQ_CONTENT"] = values["content_path"]
    report.append(
        _write(
            target / "mcp.json",
            json.dumps(mcp_cfg, indent=2) + "\n",
            overwrite,
        )
    )

    profile_tmpl = (templates / ".agent-hq" / "profile.yaml").read_text(encoding="utf-8")
    report.append(
        _write(
            target / ".agent-hq" / "profile.yaml", _render(profile_tmpl, placeholders), overwrite
        )
    )
    return report
