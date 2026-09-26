"""Agent HQ CLI entry point.

Full commands (`init`, `doctor`, `validate`, `import`) land in Phase 4;
Phase 0 ships only the version command to prove the console script works.
"""

import typer

app = typer.Typer(help="Agent HQ — manage agent guidance projects.")


@app.callback()
def _root() -> None:
    """Keep the app multi-command so `agent-hq version` works in Phase 0."""


@app.command()
def version() -> None:
    """Print the Agent HQ CLI version."""
    from agent_hq_server import __version__

    print(f"agent-hq {__version__}")


if __name__ == "__main__":
    app()
