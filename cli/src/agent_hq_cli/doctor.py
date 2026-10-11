"""`agent-hq doctor` — verify the install end-to-end: server starts, content
loads, and a bootstrap returns a non-empty bundle. Exits non-zero on any failure.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from agent_hq_server.catalog.catalog import load
from agent_hq_server.tools.bootstrap import bootstrap

from agent_hq_cli.config import content_root


def _check_server_starts(content: Path) -> tuple[bool, str]:
    """Spawn the real stdio server and complete the MCP `initialize` handshake."""
    cmd = [sys.executable, "-m", "agent_hq_server"]
    env = {
        "AGENT_HQ_CONTENT": str(content),
        "AGENT_HQ_LOG_LEVEL": "WARNING",
        **_safe_env(),
    }
    with tempfile.TemporaryDirectory() as proj:
        env["AGENT_HQ_PROJECT"] = proj
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
        )
        try:
            if proc.stdin is None:
                return False, "subprocess stdin is None"
            proc.stdin.write(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {},
                            "clientInfo": {"name": "doctor", "version": "0"},
                        },
                    }
                )
                + "\n"
            )
            proc.stdin.flush()
            line = proc.stdout.readline() if proc.stdout else None
            if not line:
                return (
                    False,
                    f"no initialize response; stderr: "
                    f"{proc.stderr.read()[-500:] if proc.stderr else ''}",
                )
            resp = json.loads(line)
            if "result" not in resp:
                return False, f"initialize error: {resp.get('error')}"
            return (
                True,
                f"serverInfo={resp['result'].get('serverInfo', {}).get('name')}",
            )
        finally:
            proc.terminate()
            proc.wait(timeout=10)


def _safe_env() -> dict[str, str]:
    from os import environ

    return dict(environ)


def run_doctor(project: Path | None, profile: str | None) -> int:
    project = (project or Path.cwd()).resolve()
    content = content_root()
    failures: list[str] = []

    # 1. content loads
    if not content.is_dir():
        print(f"✗ content tree not found at {content}")
        return 1
    catalog = load(content)
    counts = catalog.counts()
    if catalog.issues:
        failures.append(f"content issues: {[i.render() for i in catalog.issues]}")
    if not catalog.profiles:
        failures.append("no profiles found — bootstrap will fail")
    print(f"✓ content loaded: {counts} ({len(catalog.issues)} issues)")

    # 2. bootstrap returns a non-empty bundle
    bundle = bootstrap(catalog, project, pinned_profile=profile)
    if hasattr(bundle, "error"):
        # Type narrowing that Pyright accepts for hasattr
        from agent_hq_server.schema.view import ErrorView
        if isinstance(bundle, ErrorView):
            failures.append(f"bootstrap error: {bundle.error}")
    else:
        # Use type narrowing to satisfy Pyright
        from agent_hq_server.schema.bundle import Bundle
        if isinstance(bundle, Bundle):
            n_instr = len(bundle.instructions)
            n_roles = len(bundle.roles)
            n_skills = len(bundle.skills)
            if n_instr + n_roles + n_skills == 0 and bundle.workflow is None:
                failures.append("bundle is empty (no instructions, roles, skills, or workflow)")
            print(
                f"✓ bootstrap: profile={bundle.profile.id} ({bundle.profile.source}) "
                f"workflow={bundle.workflow.slug if bundle.workflow else None} "
                f"instructions={n_instr} roles={n_roles} skills={n_skills}"
            )
        else:
            failures.append("bootstrap returned an unexpected type")

    # 3. server starts (real stdio process)
    ok, detail = _check_server_starts(content)
    print(("✓ " if ok else "✗ ") + f"server: {detail}")
    if not ok:
        failures.append(detail)

    if failures:
        print(f"\n✗ doctor FAILED with {len(failures)} problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\n✓ doctor: all checks passed")
    return 0
