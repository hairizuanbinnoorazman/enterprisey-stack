"""
MCP Server with HTTP transport and manifest.json

Requirements:
    pip install "mcp[cli]" fastapi uvicorn

Run:
    python mcp_server.py
"""

from __future__ import annotations
import os
import re
import logging
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP, Context

BASE_DIR = Path(__file__).parent
NOTES_DIR = BASE_DIR / "notes"

# -----------------
# MCP Server
# -----------------
mcp = FastMCP("Demo MCP Server")

# -----------------
# Tools
# -----------------
@mcp.tool()
async def add(context: Context, a: int, b: int) -> int:
    """Add two integers and return the sum."""
    await context.info(f"DAAAAMMMMMNNN: {context.request_context.meta}")
    await context.info(f"Client ID: {context.client_id}")
    await context.info(f"Session ID: {context.session_id}")
    await context.info(f"{context.get_http_request().headers}")
    
    if hasattr(context, 'user'):
        await context.info(f"User: {context.user}")
    if hasattr(context, 'username'):
        await context.info(f"Username: {context.username}")
    if hasattr(context, 'user_id'):
        await context.info(f"User ID: {context.user_id}")
    
    await context.info(f"Context attributes: {[attr for attr in dir(context) if not attr.startswith('_')]}")
    
    await context.info(f"a: {a}")
    await context.info(f"b: {b}")
    return a + b

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=9000)
