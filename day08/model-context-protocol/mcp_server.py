from datetime import datetime
from fastmcp import FastMCP
import random
import secrets
import string

mcp = FastMCP("First MCP server")

@mcp.tool()
def current_time():
    """Return only current time or latest time"""
    return datetime.now().strftime("%d-%M-%Y %H:%M:%S")

@mcp.tool()
def roll_dice():
    """Roll a six-sided dice, can be used for ludo, snake-ladder or similar board game."""
    return random.randint(1,6)

@mcp.tool()
def generate_password(length:int = 12):
    """Generate a secure and strong password."""
    combination_of_characters = (string.ascii_letters + string.digits + string.punctuation)
    return "".join(secrets.choice(combination_of_characters) for _ in range(length))

if __name__ == "__main__":
    print("Starting the MCP server...")
    mcp.run()