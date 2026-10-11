"""Gate verification and phase ordering (technical.md §6.2).

Enforces that workflows are followed in order and that gates are satisfied
before proceeding.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from agent_hq_server.schema.workflow import Gate

log = logging.getLogger(__name__)


def verify_ordering(state: dict[str, Any], phase_id: str, workflow_phases: list[Any]) -> list[str]:
    """
    Checks if all prior phases have been completed (gates passed).
    Returns a list of flags if deviations are found.
    """
    flags = []
    # Find index of current phase
    current_idx = None
    for i, p in enumerate(workflow_phases):
        if p.id == phase_id:
            current_idx = i
            break

    if current_idx is None:
        # Phase doesn't exist in current workflow version
        return ["UNKNOWN_PHASE"]

    # Check all phases before current_idx
    for i in range(current_idx):
        prior_phase = workflow_phases[i]
        prior_id = prior_phase.id
        phase_state = state.get("phases", {}).get(prior_id, {})
        if not phase_state.get("gate_passed", False):
            flags.append(f"PRIOR_PHASE_NOT_PASSED:{prior_id}")

    return flags


def verify_gate(
    gate: Gate,
    project_path: Path,
    completed_indices: list[int],
    checklist: list[str],
    evidence: str | None,
    approved: bool = False,
) -> bool:
    """
    Evaluates a gate based on its kind.
    - manual: requires approved=True
    - artifact: requires evidence match (primitive check) or pattern match in project
    - checklist-complete: all checklist items reported completed
    - none: always passes
    """
    kind = gate.kind

    if kind == "none":
        return True

    if kind == "manual":
        return approved

    if kind == "checklist-complete":
        return len(completed_indices) >= len(checklist)

    if kind == "artifact":
        # 1. If evidence is provided and matches pattern (simple contains)
        # or if the file exists in the project
        if not gate.pattern:
            return False

        # Evidence-based check
        if evidence and gate.pattern in evidence:
            return True

        # File-system based check
        try:
            # We use a simple glob check for the pattern relative to project_path
            # Note: Gate patterns in technical.md are like 'docs/design/**'
            # We'll use project_path.glob(pattern)
            # Handle double asterisks by converting to glob if necessary, 
            # but Path.glob handles basic **
            matches = list(project_path.glob(gate.pattern))
            return len(matches) > 0
        except Exception as exc:
            log.warning("artifact gate check failed for %s: %s", gate.pattern, exc)
            return False

    return False
