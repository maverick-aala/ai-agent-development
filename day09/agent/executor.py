"""
Day 09 — Execute one planner-chosen action via MCP and normalize the result to a string for state.
"""

from model_context_protocol.mcp_client import execute_tool


async def execute_action(action, state, client):
    """
    Run one MCP tool and return its output as text for record_observation().

    The loop does not import FastMCP directly — only this module talks to execute_tool().

    Parameters:
        action (str): Tool name from the planner (e.g. "current_time"); becomes the MCP call_tool name.
        state (dict): Agent state (passed for future use; not read in the current implementation).
        client: MCP FastMCP client from connect(); used by execute_tool() to call the server.

    Returns:
        str: Tool output text from result.content[0].text, or str(result) as a fallback.
    """
    # await pauses until the MCP server finishes the tool; result is the raw FastMCP tool result object.
    result = await execute_tool(client, action)

    # hasattr() checks whether result has a .content attribute (typical MCP structured response).
    if hasattr(result, "content"):
        if result.content:
            # content[0] is the first content block; .text is the human-readable tool output string.
            return result.content[0].text

    # str(result) converts any other return shape to a string so record_observation() always gets text.
    return str(result)
