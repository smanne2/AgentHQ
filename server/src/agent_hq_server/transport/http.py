"""HTTP/SSE transport for production deployment.

MCP supports HTTP with Server-Sent Events (SSE) for streaming responses.
This enables multiple clients to connect via HTTP and communicate with the server.

Uses the SDK's built-in `run_streamable_http_async` method.
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


def configure_http_logging(log_level: str = "INFO") -> None:
    """Configure logging for HTTP server."""
    level = _LEVELS.get(log_level.upper(), logging.INFO)
    logging.basicConfig(
        stream=sys.stderr, level=level, format="%(levelname)s %(name)s: %(message)s"
    )
    # Keep SDK loggers calm
    logging.getLogger("mcp").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)


def run_http(server: Any, log_level: str = "INFO") -> None:
    """Run the server over HTTP/SSE (blocking).

    Uses FastMCP's built-in streamable HTTP transport which handles all
    SSE/JSON-RPC protocol details. Host and port are configured via FastMCP
    init parameters.

    ``server`` is a ``FastMCP`` instance.
    """
    configure_http_logging(log_level)

    import anyio

    async def serve():
        """Run HTTP server via FastMCP's streamable HTTP transport."""
        # FastMCP's run_streamable_http_async spawns an HTTP server
        # using uvicorn with settings configured at init time
        await server.run_streamable_http_async()

    anyio.run(serve)
