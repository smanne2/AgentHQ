"""Phase 0 smoke tests: workspace wiring, imports, console entry points."""


def test_server_package_importable() -> None:
    from agent_hq_server import __version__

    assert __version__ == "0.1.0"


def test_server_main_runs() -> None:
    from agent_hq_server.__main__ import main

    main()  # must not raise


def test_cli_app_exists() -> None:
    from agent_hq_cli.main import app

    assert app is not None
