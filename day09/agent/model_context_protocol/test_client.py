"""
Day 09 — Smoke test: connect, list tools, call one tool, disconnect (no agent loop).

Run from repository root so Client("day09/agent/...") path in connect() resolves.
"""

import asyncio  # Needed because connect() and execute_tool() are async functions.

from day09.agent.model_context_protocol.mcp_client import (
    connect,
    disconnect,
    discover_tools,
    execute_tool,
)


async def main():
    """
    One-shot MCP exercise.

    Parameters:
        None

    Returns:
        None
    """
    client = await connect()

    tools = await discover_tools(client)

    print("~" * 40)  # print("~" * 40) draws a line of tildes for visual separation in the terminal.
    print("Available tools")
    print("~" * 40)

    for tool in tools:
        print(tool.name)

    result = await execute_tool(
        client,
        tools[2].name if len(tools) > 0 else "roll_dice",
    )

    # result may be a structured object; print() shows its string form for a quick sanity check.
    print(f'{tools[0].name if len(tools) > 0 else "roll_dice"}: ', result)

    await disconnect(client)


asyncio.run(main())  # Runs main() and shuts down the async event loop when done.
