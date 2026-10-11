"""E2E Smoke Test for Agent HQ (Phase 7.1).

Spawns the real server over stdio and speaks JSON-RPC to verify the core
onboarding flow: initialize → bootstrap → get_checklist → report_progress.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

def run_step(client, method, params=None):
    req = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params:
        req["params"] = params
    client.stdin.write(json.dumps(req) + "\n")
    client.stdin.flush()
    # Simple wait for response
    line = client.stdout.readline()
    return json.loads(line)

def main():
    # Use the actual server
    server_cmd = [sys.executable, "-m", "agent_hq_server"]
    
    # Set environment to point to the content root in this repo
    env = os.environ.copy()
    env["AGENT_HQ_CONTENT"] = str(Path(__file__).resolve().parents[3] / "content")
    
    # Fixture project
    proj = Path("/tmp/agent-hq-e2e").resolve()
    proj.mkdir(exist_ok=True)
    (proj / "README.md").write_text("# E2E Project")
    env["AGENT_HQ_PROJECT"] = str(proj)

    proc = subprocess.Popen(
        server_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        env=env,
        text=True
    )

    try:
        print("🚀 Testing initialize...")
        resp = run_step(proc, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "e2e-script", "version": "1.0.0"},
        })
        assert "serverInfo" in resp["result"]
        print("✅ initialize OK")

        print("🚀 Testing bootstrap...")
        resp = run_step(proc, "tools/call", {
            "name": "agent_hq.bootstrap",
            "arguments": {"projectPath": str(proj)}
        })
        bundle = resp["result"]["content"][0]["text"] # FastMCP returns content list
        # FastMCP might return JSON string if result is complex
        if isinstance(bundle, str):
            bundle = json.loads(bundle)
        
        workflow_slug = bundle["workflow"]["slug"]
        print(f"✅ bootstrap OK (Workflow: {workflow_slug})")

        print("🚀 Testing get_checklist...")
        resp = run_step(proc, "tools/call", {
            "name": "agent_hq.get_checklist",
            "arguments": {"workflowSlug": workflow_slug, "phaseId": "discover"}
        })
        checklist_data = json.loads(resp["result"]["content"][0]["text"])
        print(f"✅ get_checklist OK (Phase: {checklist_data['phase_id']})")

        print("🚀 Testing report_progress...")
        resp = run_step(proc, "tools/call", {
            "name": "agent_hq.report_progress",
            "arguments": {
                "workflowSlug": workflow_slug,
                "phaseId": "discover",
                "completed": [0, 1],
                "approved": True
            }
        })
        progress_data = json.loads(resp["result"]["content"][0]["text"])
        assert progress_data["ok"] is True
        print("✅ report_progress OK")

        print("\n🎉 E2E Smoke Test Passed Successfully!")

    except Exception as e:
        print(f"\n❌ E2E Test Failed: {e}")
        sys.exit(1)
    finally:
        proc.terminate()

if __name__ == "__main__":
    main()
