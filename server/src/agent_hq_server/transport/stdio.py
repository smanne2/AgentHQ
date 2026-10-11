"""Stdio transport — the only module (with ``tools/registry.py``) importing the ``mcp`` SDK.

DD10: the Python MCP SDK's API has churned across releases; every other module
is SDK-free, so a version bump is bounded to these two files. Stdio speaks the
MCP protocol on stdout, so all diagnostics must go to **stderr**.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

_LEVELS: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


def configure_stdio_logging(log_level: str = "INFO") -> None:
    """Root logger to stderr — stdout is reserved for the MCP protocol."""
    level = _LEVELS.get(log_level.upper(), logging.INFO)
    logging.basicConfig(
        stream=sys.stderr, level=level, format="%(levelname)s %(name)s: %(message)s"
    )
    # The SDK configures its own loggers verbosely; keep stdio output calm.
    logging.getLogger("mcp").setLevel(logging.WARNING)


def run_stdio(server: Any, log_level: str = "INFO") -> None:
    """Run the server over stdio until the client disconnects (blocking).

    ``server`` is a ``FastMCP`` instance (typed as Any so this module's only
    SDK surface stays trivially obvious when auditing the dependency rule).
    """
    configure_stdio_logging(log_level)
    import anyio

    anyio.run(server.run_stdio_async)
