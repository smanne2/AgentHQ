"""Pydantic content schemas: required fields, normalization, tolerance."""

import pytest
from agent_hq_server.schema import (
    InstructionFrontmatter,
    Profile,
    RoleFrontmatter,
    SkillFrontmatter,
    WorkflowFrontmatter,
)
from pydantic import ValidationError


def test_role_requires_description() -> None:
    with pytest.raises(ValidationError):
        RoleFrontmatter.model_validate({"name": "X"})


def test_role_tolerates_unknown_client_keys() -> None:
    role = RoleFrontmatter.model_validate(
        {
            "name": "Accessibility Expert",
            "description": "a11y rules",
            "model": "GPT-4.1",
            "tools": ["search", "read"],
            "someFutureKey": 42,
        }
    )
    assert role.model == "GPT-4.1"
    assert role.tools == ["search", "read"]
    assert (role.model_extra or {}) == {"someFutureKey": 42}


def test_instruction_appl_to_string_list_and_comma() -> None:
    assert InstructionFrontmatter.model_validate(
        {"description": "d", "applyTo": "**"}
    ).apply_to == ["**"]
    assert InstructionFrontmatter.model_validate(
        {"description": "d", "applyTo": ["**/*.ts", "**/*.tsx"]}
    ).apply_to == ["**/*.ts", "**/*.tsx"]
    # awesome-copilot style: one comma-separated string (astro fixture)
    assert InstructionFrontmatter.model_validate(
        {"description": "d", "applyTo": "**/*.astro, **/*.ts"}
    ).apply_to == ["**/*.astro", "**/*.ts"]


def test_instruction_rejects_bad_apply_to_type() -> None:
    with pytest.raises(ValidationError):
        InstructionFrontmatter.model_validate({"description": "d", "applyTo": 7})


def test_skill_minimal_frontmatter() -> None:
    skill = SkillFrontmatter.model_validate(
        {"name": "code-review", "description": "review code", "license": "MIT"}
    )
    assert skill.name == "code-review"
    assert (skill.model_extra or {}) == {"license": "MIT"}


def test_workflow_happy_path() -> None:
    wf = WorkflowFrontmatter.model_validate(
        {
            "name": "Standard Feature",
            "description": "phased feature work",
            "phases": [
                {"id": "design", "checklist": ["write design"], "gate": {"kind": "manual"}},
                {
                    "id": "implement",
                    "checklist": ["code", "tests"],
                    "gate": {"kind": "artifact", "pattern": "src/**"},
                },
            ],
        }
    )
    assert [phase.id for phase in wf.phases] == ["design", "implement"]
    assert wf.phases[0].display_title == "Design"
    assert wf.phases[1].gate.pattern == "src/**"


def test_workflow_gate_artifact_requires_pattern() -> None:
    with pytest.raises(ValidationError):
        WorkflowFrontmatter.model_validate(
            {
                "description": "d",
                "phases": [{"id": "x", "gate": {"kind": "artifact"}}],
            }
        )


def test_workflow_rejects_bad_phase_id_and_duplicates() -> None:
    with pytest.raises(ValidationError):
        WorkflowFrontmatter.model_validate({"description": "d", "phases": [{"id": "Bad_ID"}]})
    with pytest.raises(ValidationError):
        WorkflowFrontmatter.model_validate(
            {
                "description": "d",
                "phases": [{"id": "x"}, {"id": "x"}],
            }
        )


def test_profile_yaml_shape_with_aliased_matches() -> None:
    profile = Profile.model_validate(
        {
            "id": "node-web",
            "name": "Node Web",
            "description": "TS/Node services",
            "matches": {
                "anyOf": [{"file": "package.json", "containsAny": ["express", "typescript"]}]
            },
            "defaults": {"workflow": "standard-feature", "roles": ["engineer"]},
        }
    )
    assert profile.id == "node-web"
    assert profile.matches is not None
    assert profile.matches.any_of[0].file == "package.json"
    assert profile.defaults.workflow == "standard-feature"


def test_profile_rejects_non_kebab_id() -> None:
    with pytest.raises(ValidationError):
        Profile.model_validate({"id": "Node Web", "description": "x"})
