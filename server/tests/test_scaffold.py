"""Phase 0 smoke tests: workspace wiring, imports, console entry points."""

import pytest
from agent_hq_server import __version__


def test_server_package_importable() -> None:

    assert __version__ == "0.1.0"


def test_server_main_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Entry point parses flags and exits cleanly (stdio mode is covered in test_mcp_stdio)."""
    from agent_hq_server.__main__ import main

    main(["--version"])  # must not raise
    out = capsys.readouterr().out
    assert "agent-hq-server" in out


def test_cli_app_exists() -> None:
    from agent_hq_cli.main import app

    assert app is not None
