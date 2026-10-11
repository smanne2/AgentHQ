"""State management tools for agents (technical.md §6.3).

Provides tools for reporting and retrieving progress through a workflow.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from agent_hq_server.catalog import Catalog
from agent_hq_server.state import gates, store

log = logging.getLogger(__name__)


def report_progress(
    catalog: Catalog,
    project_path: Path | None,
    workflow_slug: str,
    phase_id: str,
    completed: list[int],
    evidence: str | None = None,
    approved: bool = False,
) -> dict[str, Any]:
    """
    Records progress for a phase and verifies the gate.
    Returns {ok, flags, nextPhase}.
    """
    path = project_path or Path.cwd()
    workflow = catalog.find("workflow", workflow_slug)
    if not workflow:
        return {
            "ok": False,
            "flags": [f"UNKNOWN_WORKFLOW:{workflow_slug}"],
            "nextPhase": None,
        }

    # 1. Load state
    state = store.load_state(path, workflow_slug)
    phases = workflow.frontmatter.phases if hasattr(workflow.frontmatter, "phases") else []

    # 2. Verify ordering
    ordering_flags = gates.verify_ordering(state, phase_id, phases)

    # 3. Verify gate
    # Find the phase object
    phase_obj = next((p for p in phases if p.id == phase_id), None)
    if not phase_obj:
        return {"ok": False, "flags": [f"UNKNOWN_PHASE:{phase_id}"], "nextPhase": None}

    gate_passed = gates.verify_gate(
        gate=phase_obj.gate,
        project_path=path,
        completed_indices=completed,
        checklist=phase_obj.checklist,
        evidence=evidence,
        approved=approved,
    )

    # 4. Update state
    phase_state = state.get("phases", {}).get(phase_id, {})
    phase_state.update(
        {
            "completed": completed,
            "evidence": evidence,
            "approved": approved,
            "gate_passed": gate_passed,
            "timestamp": time.time(),
        }
    )
    state.setdefault("phases", {})[phase_id] = phase_state
    store.save_state(path, workflow_slug, state)

    # Determine next phase
    next_phase = None
    for i, p in enumerate(phases):
        if p.id == phase_id and i + 1 < len(phases):
            next_phase = phases[i + 1].id
            break

    flags = ordering_flags + ([] if gate_passed else [f"GATE_NOT_PASSED:{phase_obj.gate.kind}"])

    return {
        "ok": len(flags) == 0,
        "flags": flags,
        "nextPhase": next_phase,
    }


def get_progress(
    project_path: Path | None,
    workflow_slug: str | None = None,
) -> dict[str, Any]:
    """
    Returns the current progress board for a project.
    """
    path = project_path or Path.cwd()
    # If slug not provided, we can't load a specific state file,
    # but we could potentially list all state files for the project.
    # For now, we require slug for a specific view, or return empty if not found.
    if not workflow_slug:
        return {"error": "workflowSlug is required to get progress"}

    state = store.load_state(path, workflow_slug)
    return {
        "workflow": workflow_slug,
        "project": str(path),
        "phases": state.get("phases", {}),
    }
