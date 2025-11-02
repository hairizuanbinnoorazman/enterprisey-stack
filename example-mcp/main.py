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
    print(f"Client ID: {context.client_id}")
    print(f"Session ID: {context.session_id}")
    
    if hasattr(context, 'user'):
        print(f"User: {context.user}")
    if hasattr(context, 'username'):
        print(f"Username: {context.username}")
    if hasattr(context, 'user_id'):
        print(f"User ID: {context.user_id}")
    
    print(f"Context attributes: {[attr for attr in dir(context) if not attr.startswith('_')]}")
    
    print(f"a: {a}")
    print(f"b: {b}")
    return a + b

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=9000)
