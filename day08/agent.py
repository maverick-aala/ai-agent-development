"""
Day 08 — MCP tools: discover on server, plan with LLM, execute via MCP, respond with LLM.

Uses `llm_client` for chat completions and `mcp_client` in main() for FastMCP (two different clients).
"""

import os  # Read BASE_URL, API_KEY, and model names from os.environ after load_dotenv().

from openai import OpenAI
# Alternative: `import ollama` — Ollama-only. Alternative: raw HTTP (`httpx`) — more boilerplate.
# We use the OpenAI SDK: Ollama and many hosts expose an OpenAI-compatible API (same code locally and in the cloud).

from dotenv import load_dotenv
# Alternative: export variables in the shell; `.env` keeps secrets out of source code.

import asyncio  # MCP I/O is async; asyncio.run() starts the event loop from __main__.

from model_context_protocol.mcp_client import connect, disconnect, discover_tools, execute_tool

# Load key/value pairs from `.env` in the working directory into os.environ.
load_dotenv()

# HTTP client for the language model — points at Ollama or another OpenAI-compatible server (not always api.openai.com).
llm_client = OpenAI(
    base_url=os.getenv("BASE_URL"),  # Often http://localhost:11434/v1 for Ollama.
    api_key=os.getenv("API_KEY"),  # Any placeholder for local Ollama; real key for OpenAI cloud — keep in .env.
)
# Same client pattern as Days 01–07; renamed to llm_client to distinguish from the MCP client in main().
# Alternative: `OpenAI()` with no base_url (OpenAI cloud only). Alternative: AsyncOpenAI for async servers.


async def main():
    mcp_client = await connect()  # Day 08 only: FastMCP session to mcp_server.py.

    tools = await discover_tools(mcp_client)

    print("~" * 40)
    print("Available Tools")
    print("~" * 40)

    for tool in tools:
        print(tool.name)

    user_request = input("User: ")

    tool_name = planner(user_request, tools)
    print("Tool name: ", tool_name)

    tool_result = await execute_tool(mcp_client, tool_name)
    print("Tool Result: ", tool_result)

    final_answer = generate_response(user_request, tool_result)
    print()
    print("AI: ", final_answer)
    print()

    await disconnect(mcp_client)


def build_tool_descriptions(tools):
    descriptions = ""
    for tool in tools:
        descriptions += f"""Tool: {tool.name} Description: {tool.description}"""

    return descriptions


def planner(user_request, tools):
    tool_descriptions = build_tool_descriptions(tools)
    prompt = f"""
                You are an AI Planner.
                Available Tools
                {tool_descriptions}
                Instruction
                1. Select the best tool.
                2. Reply ONLY with the tool name without keyword "Tool:"
                3. Do not explain.

                User Request: {user_request}
            """
    response = llm_client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),  # Chat model from .env (Day 06+; separate from EMBEDDING_MODEL).
        messages=[
            {
                "role": "user",  # Human turn in the chat API.
                "content": prompt,
            }
        ],
    )
    # Alternative: stream=True. Chat Completions stays consistent across Days 01–08 for Ollama compatibility.

    tool_name = response.choices[0].message.content  # First choice text; may be None if output is empty.
    return tool_name.strip()


def generate_response(user_request, tool_result):
    prompt = f"""
                The User asked: {user_request}
                The tool returned: {tool_result}
                If user question is related to tool then include that in response and Answer in natural language
            """
    response = llm_client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),  # Chat model from .env (Day 06+; separate from EMBEDDING_MODEL).
        messages=[
            {
                "role": "user",  # Human turn in the chat API.
                "content": prompt,
            }
        ],
    )
    # Alternative: stream=True. Chat Completions stays consistent across Days 01–08 for Ollama compatibility.

    return response.choices[0].message.content  # First choice text; may be None if output is empty.


if __name__ == "__main__":
    asyncio.run(main())
