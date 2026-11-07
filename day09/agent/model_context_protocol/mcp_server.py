"""
Day 09 — FastMCP server: registers Python functions as MCP tools (time, dice, password).

Run standalone with `python mcp_server.py` or let the FastMCP Client spawn this file from connect().
"""

from datetime import datetime  # datetime.now() for current_time tool output.
from fastmcp import FastMCP  # Decorator @mcp.tool() exposes functions over MCP.
import random  # random.randint for roll_dice.
import secrets  # secrets.token_urlsafe for cryptographically strong passwords.
import string  # Imported in Day 08 variant; unused here but kept for parity with course tools.

# FastMCP("...") creates a named server instance tools attach to.
mcp = FastMCP("First MCP server")


@mcp.tool()  # Registers the next function as an MCP-callable tool with docstring = description.
def current_time():
    """Return only current time or latest time"""
    return datetime.now().strftime("%d-%M-%Y %H:%M:%S")


@mcp.tool()
def roll_dice():
    """Roll a six-sided dice, can be used for ludo, snake-ladder or similar board game."""
    return random.randint(1, 6)


@mcp.tool()
def generate_password(length: int = 12):
    """Generate a secure password. Whenever user ask for new, strong, or safe password."""
    return secrets.token_urlsafe(length)


if __name__ == "__main__":
    print("Starting the MCP server...")  # print() tells the operator the server process is starting.
    mcp.run()  # Blocks and serves MCP (typically stdio) until the process exits.
