from fastmcp import Client

async def connect():
    """Connect to the MCP Server"""
    
    client = Client("day08/model-context-protocol/mcp_server.py")
    await client.__aenter__()
    print("Connected to the MCP Server")
    return client

async def disconnect(client):
    """Close the MCP connection. """

    # exception type, exception value and exception traceback
    await client.__aexit__ (
        None, None, None
    )

async def discover_tools(client):
    """Retrieve all tools from the MCP server."""

    tools = await client.list_tools()
    return tools

async def execute_tool(client, tool_name, arguments=None):
    """Execute tool."""
    if arguments is None:
        arguments = {}
    
    result = await client.call_tool(
        tool_name,
        arguments
    )

    return result
