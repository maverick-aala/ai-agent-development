"""
Day 09 — Entry point: connect MCP, list tools, run run_agent_loop(), print final answer, disconnect.

Naming note:
  - Module-level `client` below is the OpenAI SDK client (chat completions for format_answer).
  - In main(), `client` is rebound to the MCP client — only inside main(); format_answer() still uses OpenAI `client`.
"""

import os  # Read BASE_URL, API_KEY, and model names from os.environ after load_dotenv().

from openai import OpenAI
# Alternative: `import ollama` — Ollama-only. Alternative: raw HTTP (`httpx`) — more boilerplate.
# We use the OpenAI SDK: Ollama and many hosts expose an OpenAI-compatible API (same code locally and in the cloud).

from dotenv import load_dotenv
# Alternative: export variables in the shell; `.env` keeps secrets out of source code.

import asyncio  # MCP and run_agent_loop are async; asyncio.run(main()) starts the event loop.

from model_context_protocol.mcp_client import connect, disconnect, discover_tools
from planner import planner
from executor import execute_action
from loop import run_agent_loop

# Load key/value pairs from `.env` in the working directory into os.environ.
load_dotenv()

# HTTP client for the language model — points at Ollama or another OpenAI-compatible server (not always api.openai.com).
client = OpenAI(
    base_url=os.getenv("BASE_URL"),  # Often http://localhost:11434/v1 for Ollama.
    api_key=os.getenv("API_KEY"),  # Any placeholder for local Ollama; real key for OpenAI cloud — keep in .env.
)
# Alternative: `OpenAI()` with no base_url (OpenAI cloud only). Alternative: AsyncOpenAI for async servers.


def format_answer(state):
    """
    After FINISH, call the LLM once to turn state (actions + observations) into a user-friendly reply.

    Parameters:
        state (dict): Full agent state; uses user_request, actions, and observations in the prompt.

    Returns:
        str: Stripped assistant message — stored as final_answer by finish() in the loop.
    """
    prompt = f"""
                The user asked: {state["user_request"]}
                Actions performed: {state["actions"]}    
                Observations: {state["observations"]}

                Answer the user naturally.

                Do not mention internal planning.
                Do not mention state.
                Do not memntion tools.
                Do not bloat the answer with the extra details.
            """

    response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),  # Chat model from .env (Day 06+; separate from EMBEDDING_MODEL).
        messages=[
            {
                "role": "user",  # Human turn in the chat API.
                "content": prompt,
            }
        ],
    )
    # Alternative: stream=True. Chat Completions stays consistent across Days 01–08 for Ollama compatibility.

    return response.choices[0].message.content.strip()  # First choice text; may be None if output is empty.


async def main():
    """
    Wire MCP session, user input, agent loop, and cleanup.

    Parameters:
        None — reads user input from stdin.

    Returns:
        None
    """
    # await connect() starts the MCP client and attaches to mcp_server.py.
    client = await connect()
    tools = await discover_tools(client)

    # print() shows a blank line then a header so tool names are easy to read in the terminal.
    print()
    print("Available Tools")
    print("------------")

    for tool in tools:
        print(tool.name)  # Each tool.name is an MCP tool the planner may choose.

    user_request = input("\nUser: ")  # input() waits for you to type the task and press Enter.

    state = await run_agent_loop(
        user_request,
        planner,
        execute_action,
        format_answer,
        tools,
        client,
    )

    print()
    print("Final Answer: ")
    print(state["final_answer"])

    await disconnect(client)  # Closes the MCP session cleanly.


# __name__ == "__main__" is True when you run `python runner.py` directly (not when imported).
if __name__ == "__main__":
    asyncio.run(main())  # asyncio.run() executes main() and manages the async event loop.
