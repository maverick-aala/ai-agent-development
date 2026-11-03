"""Day 08 — Async helpers for FastMCP (connect, list tools, call tool)."""

from fastmcp import Client


async def connect():
    """Open MCP session to the local server module."""
    client = Client("day08/model_context_protocol/mcp_server.py")
    await client.__aenter__()
    print("Connected to the MCP Server")
    return client


async def disconnect(client):
    """Close MCP session."""
    await client.__aexit__(None, None, None)


async def discover_tools(client):
    """Return tool metadata from the MCP server."""
    tools = await client.list_tools()
    return tools


async def execute_tool(client, tool_name, arguments=None):
    """Invoke tool_name on the MCP server; return first text content part."""
    if arguments is None:
        arguments = {}

    result = await client.call_tool(tool_name, arguments)

    return result.content[0].text
