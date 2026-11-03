"""Day 08 — Smoke test MCP client without full agent.py."""

import asyncio
from mcp_client import connect, disconnect, discover_tools, execute_tool


async def main():
    client = await connect()

    tools = await discover_tools(client)

    print("~" * 40)
    print("Available tools")
    print("~" * 40)

    for tool in tools:
        print(tool.name)

    result = await execute_tool(
        client,
        tools[2].name if len(tools) > 0 else "roll_dice",
    )

    print(f'{tools[0].name if len(tools) > 0 else "roll_dice"}: ', result)

    await disconnect(client)


asyncio.run(main())
