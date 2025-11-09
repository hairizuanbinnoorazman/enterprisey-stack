"""
MCP Server with HTTP transport and manifest.json

Requirements:
    pip install "mcp[cli]" fastapi uvicorn

Run:
    python mcp_server.py
"""

from __future__ import annotations
from typing import Any, Dict
import os
import re
import requests
from pathlib import Path
from typing import Optional
import jwt
from jwt import PyJWKClient

from fastmcp import FastMCP, Context
from fastmcp.utilities import logging

BASE_DIR = Path(__file__).parent
NOTES_DIR = BASE_DIR / "notes"

# -----------------
# MCP Server
# -----------------
mcp = FastMCP("Demo MCP Server")

# Setting environment variables
OIDC_CLIENT_ID: str = os.environ["OIDC_CLIENT_ID"]
OIDC_CLIENT_SECRET: str = os.environ["OIDC_CLIENT_SECRET"]
OIDC_ISSUER: str = os.environ["OIDC_ISSUER"]

logger = logging.get_logger('MAIN')
logger.info(OIDC_CLIENT_ID)
logger.info(OIDC_CLIENT_SECRET)
logger.info(OIDC_ISSUER)
JWKS_URI = requests.get(f"{OIDC_ISSUER}/.well-known/openid-configuration").json()["jwks_uri"]

async def retrieve_user(context: Context) -> None:
    if context.request_context.meta is not None:
        ll = context.request_context.meta.model_dump()
        await context.info(f"Context Meta 0 :: {context.request_context.meta is not None}")
        await context.info(f"Context Meta 1 :: {ll}")
        await context.info(f"Context Meta 2 :: {ll.keys()}")
        await context.info(f"Context Meta 3 :: {ll['headers']}")
        await context.info(f"Context Meta 4 :: {ll['headers'].keys()}")
        await context.info(f"Context Meta 5 :: {ll['headers']['authorization']}")
        authorization_val: str = ll['headers']['authorization']
        authorization_val = authorization_val.split(' ')[1]
        jwks_client = PyJWKClient(JWKS_URI)
        signing_key = jwks_client.get_signing_key_from_jwt(authorization_val)
        decoded = jwt.decode(authorization_val, signing_key.key, algorithms=["RS256"], audience=OIDC_CLIENT_ID, issuer=OIDC_ISSUER)
        await context.info(f"Context Meta 6 :: {decoded}")
        await context.info(f"Context Meta 7 :: {decoded['email']}")


# -----------------
# Tools
# -----------------
@mcp.tool()
async def add(context: Context, a: int, b: int) -> int:
    """Add two integers and return the sum."""
    await context.info(f"DAAAAMMMMMNNN: {context.request_context.meta}")
    await retrieve_user(context)
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
