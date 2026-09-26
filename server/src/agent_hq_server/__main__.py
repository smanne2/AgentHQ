"""Entry point: ``agent-hq-server`` — config → catalog → registry → stdio.

Diagnostic output goes to stderr only; stdout is reserved for the MCP
protocol. All paths are overridable via env (see ``config.py``).
"""

from __future__ import annotations

import argparse
import sys

from agent_hq_server import __version__
from agent_hq_server.config import build
from agent_hq_server.tools.registry import create_server
from agent_hq_server.transport.stdio import run_stdio


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(
        prog="agent-hq-server",
        description="Agent HQ MCP server (stdio). "
        "Env: AGENT_HQ_CONTENT, AGENT_HQ_PROJECT, AGENT_HQ_LOG_LEVEL, AGENT_HQ_PROFILE.",
    )
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument(
        "--content", default=None, help="content tree path (default: env/repo content/)"
    )
    parser.add_argument(
        "--project", default=None, help="default project path for bootstrap"
    )
    parser.add_argument(
        "--log-level", default=None, help="DEBUG, INFO (default), WARNING, ERROR"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.version:
        print(f"agent-hq-server {__version__}")  # explicit flag = not in protocol mode
        return

    config = build(
        content_path=args.content, project_path=args.project, log_level=args.log_level
    )
    server = create_server(config)
    run_stdio(server, config.log_level)


if __name__ == "__main__":
    main()
