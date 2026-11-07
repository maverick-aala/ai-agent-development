"""
Day 09 — Async helpers for FastMCP: connect, list tools, call tool, disconnect.

Same responsibilities as Day 08 mcp_client.py; paths point at day09 server.
execute_tool() returns the full MCP result object (Day 09 executor.py extracts .text).
"""

from fastmcp import Client  # Client speaks MCP to a server script or URL.


async def connect():
    """
    Open an MCP session by spawning / attaching to the local FastMCP server module.

    Parameters:
        None

    Returns:
        Client: Connected FastMCP client; pass to discover_tools, execute_tool, disconnect.
    """
    # Client(...) takes a path to mcp_server.py relative to the process working directory (usually repo root).
    client = Client("day09/agent/model_context_protocol/mcp_server.py")
    await client.__aenter__()  # Manual async context enter (same as `async with Client(...) as client`).
    print("Connected to the MCP Server")  # print() confirms connection in the terminal.
    return client


async def disconnect(client):
    """
    Close the MCP session and release resources.

    Parameters:
        client: FastMCP client previously returned from connect().

    Returns:
        None
    """
    await client.__aexit__(None, None, None)  # (exc_type, exc_val, exc_tb) — None means no active exception.


async def discover_tools(client):
    """
    Ask the server which tools exist (name, description, JSON schema).

    Parameters:
        client: Connected FastMCP client.

    Returns:
        list: Tool metadata objects (use .name and .description in the planner).
    """
    tools = await client.list_tools()  # MCP protocol method tools/list.
    return tools


async def execute_tool(client, tool_name, arguments=None):
    """
    Invoke one MCP tool by name.

    Parameters:
        client: Connected FastMCP client.
        tool_name (str): Registered tool name on the server (e.g. "roll_dice").
        arguments (dict, optional): Tool parameters; default {} when the tool needs no args.

    Returns:
        Tool result object from FastMCP (often has .content with .text parts).
    """
    if arguments is None:
        arguments = {}  # Avoid mutable default; MCP expects a dict of parameters.

    result = await client.call_tool(tool_name, arguments)  # MCP tools/call.

    return result  # Day 09: return full object; executor.execute_action() pulls out text.
