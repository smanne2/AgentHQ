"""End-to-end MCP stdio round-trip (Phase 2 acceptance, technical.md §2 task 2.11).

Spawns the real ``agent-hq-server`` console script as a subprocess and speaks
line-delimited JSON-RPC to it — the same wire path MCP Inspector / VS Code /
Cline use: initialize → tools/list (all 11 names) → call every tool.
"""

from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import IO

import pytest

FIXTURES = Path(__file__).parent / "fixtures" / "content"
TIMEOUT = 20.0

EXPECTED_TOOLS = {
    "agent_hq.bootstrap",
    "agent_hq.content_info",
    "agent_hq.list_roles",
    "agent_hq.get_role",
    "agent_hq.list_instructions",
    "agent_hq.get_instruction",
    "agent_hq.list_skills",
    "agent_hq.get_skill",
    "agent_hq.list_workflows",
    "agent_hq.get_workflow",
    "agent_hq.get_checklist",
}


class _Client:
    """Minimal stdio JSON-RPC client: one request at a time, line-framed."""

    def __init__(self, proc: subprocess.Popen) -> None:
        self.proc = proc
        self._next_id = 0
        # A reader thread owns the blocking stdout read; `select` on a pipe is
        # unreliable for text-mode wrappers in some environments (tty/CI).
        self._lines: queue.Queue[str | None] = queue.Queue()
        assert proc.stdout is not None
        threading.Thread(target=self._read_stdout, args=(proc.stdout,), daemon=True).start()

    def _send(self, message: dict) -> None:
        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()

    def _read_stdout(self, stream: IO[str]) -> None:
        """Copy stdout lines into the queue until the stream closes."""
        for line in stream:
            self._lines.put(str(line))
        self._lines.put(None)  # sentinel: server closed stdout

    def _receive(self, deadline: float) -> dict:
        remaining = deadline - _now()
        if remaining <= 0:
            raise TimeoutError("no MCP response within deadline")
        try:
            line = self._lines.get(timeout=remaining)
        except queue.Empty as exc:
            raise TimeoutError("no MCP response within deadline") from exc
        if line is None:
            raise AssertionError(f"server closed stdout; stderr: {self._drain_stderr()}")
        return json.loads(line)

    def request(self, method: str, params: dict | None = None, timeout: float = TIMEOUT) -> dict:
        self._next_id += 1
        envelope = {"jsonrpc": "2.0", "id": self._next_id, "method": method}
        if params is not None:
            envelope["params"] = params
        self._send(envelope)
        deadline = _now() + timeout  # absolute: `_receive` expects a monotonic deadline
        while True:
            message = self._receive(deadline)
            if message.get("id") == self._next_id:
                if "error" in message:
                    raise AssertionError(f"{method} failed: {message['error']}")
                return message["result"]

    def notify(self, method: str) -> None:
        self._send({"jsonrpc": "2.0", "method": method})

    def _drain_stderr(self) -> str:
        assert self.proc.stderr is not None
        return self.proc.stderr.read()[-4000:]


def _now() -> float:
    import time

    return time.monotonic()


@pytest.fixture()
def project_dir(tmp_path: Path) -> Path:
    project = tmp_path / "demo-project"
    (project / "src").mkdir(parents=True)
    (project / "README.md").write_text("# demo\n", encoding="utf-8")
    return project


def _spawn(project_dir: Path) -> subprocess.Popen:
    env = {
        **os.environ,
        "AGENT_HQ_CONTENT": str(FIXTURES),
        "AGENT_HQ_PROJECT": str(project_dir),
        "AGENT_HQ_LOG_LEVEL": "WARNING",
    }
    return subprocess.Popen(
        [sys.executable, "-m", "agent_hq_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
    )


def _call(client: _Client, name: str, arguments: dict | None = None) -> dict:
    return client.request("tools/call", {"name": name, "arguments": arguments or {}})


def test_mcp_stdio_full_roundtrip(project_dir: Path) -> None:
    proc = _spawn(project_dir)
    try:
        client = _Client(proc)
        deadline = _now() + TIMEOUT

        init = client.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "pytest-client", "version": "0.1.0"},
            },
        )
        assert init["serverInfo"]["name"] == "agent-hq"
        client.notify("notifications/initialized")

        listed = client.request("tools/list")["tools"]
        names = {t["name"] for t in listed}
        assert names == EXPECTED_TOOLS
        for tool in listed:  # every schema must be a valid object schema
            assert tool["inputSchema"].get("type") == "object"

        info = _call(client, "agent_hq.content_info")
        counts = info["structuredContent"]["counts"]
        assert counts == {
            "roles": 3,
            "instructions": 3,
            "skills": 2,
            "workflows": 1,
            "profiles": 1,
        }
        assert info["structuredContent"]["profile_ids"] == ["default"]

        bootstrap = _call(client, "agent_hq.bootstrap", {"projectPath": str(project_dir)})
        assert bootstrap["isError"] is False
        bundle = bootstrap["structuredContent"]
        assert bundle["profile"] == {
            "id": "default",
            "name": "Default",
            "source": "fallback",
        }
        assert bundle["workflow"]["slug"] == "standard-feature"
        assert [p["id"] for p in bundle["workflow"]["phases"]] == [
            "discover",
            "design",
            "implement",
            "review",
            "ship",
        ]
        # The profile (default) inlines its listed instructions; the catalog
        # holds more (a11y, astro) — those surface via list/get tools.
        assert {i["slug"] for i in bundle["instructions"]} == {"agent-safety"}
        assert "Start phase 'discover'" in bundle["next_action"]

        roles = _call(client, "agent_hq.list_roles")["structuredContent"]["roles"]
        assert {r["slug"] for r in roles} == {
            "accessibility",
            "address-comments",
            "adr-generator",
        }
        role = _call(client, "agent_hq.get_role", {"slug": "adr-generator"})["structuredContent"]
        assert role["name"] == "ADR Generator" and "ADR" in role["body"]

        instructions = _call(client, "agent_hq.list_instructions")["structuredContent"][
            "instructions"
        ]
        assert {i["slug"] for i in instructions} == {"a11y", "agent-safety", "astro"}
        instruction = _call(client, "agent_hq.get_instruction", {"slug": "astro"})[
            "structuredContent"
        ]
        assert instruction["apply_to"][0] == "**/*.astro"

        skills = _call(client, "agent_hq.list_skills")["structuredContent"]["skills"]
        assert {s["slug"] for s in skills} == {
            "acquire-codebase-knowledge",
            "code-review",
        }
        skill = _call(client, "agent_hq.get_skill", {"slug": "code-review"})["structuredContent"]
        assert skill["body"] and isinstance(skill["files"], list)

        workflows = _call(client, "agent_hq.list_workflows")["structuredContent"]["workflows"]
        assert workflows[0]["phases"][0] == {
            "id": "discover",
            "title": "Discovery & Context",
        }
        workflow = _call(client, "agent_hq.get_workflow", {"slug": "standard-feature"})[
            "structuredContent"
        ]
        assert len(workflow["phases"]) == 5
        checklist = _call(
            client,
            "agent_hq.get_checklist",
            {"workflowSlug": "standard-feature", "phaseId": "design"},
        )["structuredContent"]
        assert checklist["gate"] == {"kind": "artifact", "pattern": "docs/design/**"}
        assert checklist["next_after_pass"] == "implement"
        assert "design note" in (checklist["body_section"] or "")

        # Unknown slugs are typed errors, not failures of the call itself.
        unknown = _call(client, "agent_hq.get_role", {"slug": "nope"})
        assert unknown["isError"] is False
        assert "no role with slug 'nope'" in unknown["structuredContent"]["error"]
        assert "adr-generator" in unknown["structuredContent"]["known_slugs"]

        assert _now() < deadline + 5
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def test_mcp_stdio_invalid_tool_is_tool_error(project_dir: Path) -> None:
    proc = _spawn(project_dir)
    try:
        client = _Client(proc)
        client.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "pytest-client", "version": "0.1.0"},
            },
        )
        client.notify("notifications/initialized")
        # SDK 1.30+ surfaces unknown tools as a tool-level error (result with
        # isError=True), not a JSON-RPC protocol error.
        result = client.request("tools/call", {"name": "agent_hq.does_not_exist"})
        assert result["isError"] is True
        assert "Unknown tool" in result["content"][0]["text"]
    finally:
        proc.terminate()
        proc.wait(timeout=10)
