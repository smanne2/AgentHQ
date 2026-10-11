"""Agent HQ CLI — `agent-hq init/doctor/validate/import/version`.

One module per command (init_cmd, doctor, validate, import_cmd); this file only
declares the typer app and command signatures, so the wiring stays tiny.
"""

from __future__ import annotations

from pathlib import Path

import typer

from agent_hq_cli import doctor as doctor_cmd
from agent_hq_cli import import_cmd
from agent_hq_cli import validate as validate_cmd
from agent_hq_cli.init_cmd import _detect, init_project

app = typer.Typer(
    help="Agent HQ — scaffold and validate governed-agent projects.",
    no_args_is_help=True,
    add_completion=False,
)


@app.command()
def version() -> None:
    """Print the Agent HQ CLI version."""
    from agent_hq_server import __version__

    print(f"agent-hq {__version__}")


@app.command()
def init(
    dir: Path = typer.Argument(None, help="Project directory to scaffold (default: CWD)."),
    profile: str = typer.Option(
        None, "--profile", "-p", help="Pin this profile id (default: detected)."
    ),
    stack: str = typer.Option(None, "--stack", help="Override the detected stack label."),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files."),
) -> None:
    """Write AGENTS.md, mcp.json, and .agent-hq/profile.yaml into a project."""
    # Re-declare as typer arguments/options for the backend runner
    # but let's see if we can just use Defaults or fix them the "Typer way"

    """Write AGENTS.md, mcp.json, and .agent-hq/profile.yaml into a project."""
    dir = dir.resolve()
    detected_stack, detected_profile = _detect(dir)
    stack = stack or detected_stack
    profile = profile or detected_profile
    for line in init_project(dir, profile, stack, force):
        print(line)
    print(f"\ninit complete: stack={stack} profile={profile}")
    print("next: `agent-hq doctor` to verify the install.")


@app.command()
def doctor(
    project: Path = typer.Option(None, "--project", help="Project to test (default: CWD)."),
    profile: str = typer.Option(None, "--profile", help="Force this profile id."),
) -> None:
    """Verify server starts, content loads, and a bundle is non-empty."""
    raise typer.Exit(doctor_cmd.run_doctor(project, profile))


@app.command()
def validate(
    path: Path = typer.Argument(None, help="Content tree to check (default: repo content/)."),
) -> None:
    """Schema-check the whole content tree (contributor gate)."""
    raise typer.Exit(validate_cmd.run_validate(path))


@app.command("import")
def import_content(
    source: Path = typer.Argument(
        ..., help="Path to community content (e.g. an awesome-copilot clone)."
    ),
    target: Path = typer.Argument(
        Path("content"), help="Content tree to import into (default: content/)."
    ),
    copy: bool = typer.Option(False, "--copy", help="Actually copy (default: dry-run)."),
) -> None:
    """Bring community content files into the content tree (dry-run by default)."""
    raise typer.Exit(import_cmd.run_import(source, target, copy))


if __name__ == "__main__":
    app()
