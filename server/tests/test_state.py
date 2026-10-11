"""Tests for state persistence and gate verification (Phase 6.4)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from agent_hq_server.catalog import load
from agent_hq_server.schema import Gate, Phase
from agent_hq_server.state import gates, store
from agent_hq_server.tools import state as state_tools


@pytest.fixture
def temp_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_catalog(tmp_path):
    # Create a dummy content tree
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    workflows_dir = content_dir / "workflows"
    workflows_dir.mkdir()

    # Standard Feature-like workflow
    wf_file = workflows_dir / "test.workflow.md"
    wf_file.write_text(
        "---\nname: Test\ndescription: Test Workflow\nphases:\n"
        "  - id: p1\n    checklist: [a, b]\n    gate: { kind: manual }\n"
        "  - id: p2\n    checklist: [c]\n    gate: { kind: checklist-complete }\n"
        "  - id: p3\n    checklist: [d]\n    gate: { kind: artifact, pattern: 'docs/*' }\n"
        "---\n",
        encoding="utf-8",
    )
    return load(content_dir)


def test_state_persistence(temp_project):
    project_path = temp_project
    slug = "test-wf"
    data = {"phases": {"p1": {"gate_passed": True}}}

    store.save_state(project_path, slug, data)
    loaded = store.load_state(project_path, slug)
    assert loaded == data


def test_ordering_verification():
    # Setup: a list of Phase objects
    phases = [
        Phase(id="p1", checklist=[], gate=Gate(kind="none")),
        Phase(id="p2", checklist=[], gate=Gate(kind="none")),
        Phase(id="p3", checklist=[], gate=Gate(kind="none")),
    ]

    # Case 1: Phase 1 not passed, trying to do Phase 2
    state = {"phases": {"p1": {"gate_passed": False}}}
    flags = gates.verify_ordering(state, "p2", phases)
    assert "PRIOR_PHASE_NOT_PASSED:p1" in flags

    # Case 2: Phase 1 passed, trying to do Phase 2
    state = {"phases": {"p1": {"gate_passed": True}}}
    flags = gates.verify_ordering(state, "p2", phases)
    assert not flags


def test_gate_kinds(temp_project):
    project_path = temp_project

    # Manual gate
    assert (
        gates.verify_gate(
            Gate(kind="manual"), project_path, [], [], None, approved=True
        )
        is True
    )
    assert (
        gates.verify_gate(
            Gate(kind="manual"), project_path, [], [], None, approved=False
        )
        is False
    )

    # Checklist gate
    assert (
        gates.verify_gate(
            Gate(kind="checklist-complete"), project_path, [0, 1], ["a", "b"], None
        )
        is True
    )
    assert (
        gates.verify_gate(
            Gate(kind="checklist-complete"), project_path, [0], ["a", "b"], None
        )
        is False
    )

    # Artifact gate (file exists)
    docs_dir = project_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "design.md").write_text("content")
    assert (
        gates.verify_gate(
            Gate(kind="artifact", pattern="docs/*"), project_path, [], [], None
        )
        is True
    )
    assert (
        gates.verify_gate(
            Gate(kind="artifact", pattern="missing/*"), project_path, [], [], None
        )
        is False
    )


def test_report_progress_tamper(mock_catalog, temp_project):
    project_path = temp_project

    # Attempt to report p2 without p1 passed
    # We need the actual Catalog object to use the tool
    result = state_tools.report_progress(
        catalog=mock_catalog,
        project_path=project_path,
        workflow_slug="test",
        phase_id="p2",
        completed=[0],
        evidence=None,
        approved=False,
    )

    assert result["ok"] is False
    assert any("PRIOR_PHASE_NOT_PASSED:p1" in f for f in result["flags"])
