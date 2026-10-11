"""MCP tool handlers (technical.md §5). No `mcp` SDK imports here — only pydantic.

Each module owns the semantics of one content kind; ``registry`` is the only
module that knows about FastMCP (DD10 SDK isolation).
"""
