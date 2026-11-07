"""
Day 09 — LLM planner: reads agent state + MCP tool list and returns the next tool name or FINISH.
"""

import os  # Read BASE_URL, API_KEY, and model names from os.environ after load_dotenv().

from openai import OpenAI
# Alternative: `import ollama` — Ollama-only. Alternative: raw HTTP (`httpx`) — more boilerplate.
# We use the OpenAI SDK: Ollama and many hosts expose an OpenAI-compatible API (same code locally and in the cloud).

from dotenv import load_dotenv
# Alternative: export variables in the shell; `.env` keeps secrets out of source code.

# Load key/value pairs from `.env` in the working directory into os.environ.
load_dotenv()

# HTTP client for the language model — points at Ollama or another OpenAI-compatible server (not always api.openai.com).
client = OpenAI(
    base_url=os.getenv("BASE_URL"),  # Often http://localhost:11434/v1 for Ollama.
    api_key=os.getenv("API_KEY"),  # Any placeholder for local Ollama; real key for OpenAI cloud — keep in .env.
)
# Alternative: `OpenAI()` with no base_url (OpenAI cloud only). Alternative: AsyncOpenAI for async servers.


def build_tool_descriptions(tools):
    """
    Turn MCP tool objects into one string for the planner prompt.

    Parameters:
        tools (list): Items from discover_tools(); each has .name and .description.

    Returns:
        str: Concatenated "Tool: ... Description: ..." lines.
    """
    descriptions = ""
    for tool in tools:
        descriptions += f"""Tool: {tool.name} 
                            Description: {tool.description}"""
    return descriptions


def planner(state, tools):
    """
    Call the chat model to pick the single next MCP tool (or FINISH).

    Parameters:
        state (dict): Agent state from state.py (user_request, actions, observations, ...).
        tools (list): MCP tools available on the server this run.

    Returns:
        str: Stripped tool name (must match MCP) or the word FINISH.
    """
    tool_descriptions = build_tool_descriptions(tools)

    prompt = f"""
                You are an AI Planner
                Your job is to decide ONLY the next action/tool.

                User request: {state["user_request"]}
                Completed Actions: {state["actions"]}
                Previous Observations: {state["observations"]}
                Available Tools: {tool_descriptions}

                Rules:
                1. Choose only one next action/tool.
                2. Never repeat an action/tool that has already been completed.
                3. Use the observations to decide what is still required.
                4. If the user's request has been completely satisfied, return FINISH.
                5. Return ONLY the tool name or FINISH.
                6. Do not bloat your answer with extra details.
                7. Return only One tool name at a time, any tool name should not be come with FINISH
                8. Don't assume anything

                Next Action:
                """

    response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),  # Chat model from .env (Day 06+; separate from EMBEDDING_MODEL).
        messages=[
            {
                "role": "system",  # Persona/instructions that steer all following replies (Day 03+).
                "content": "Your are an AI planner.",
            },
            {
                "role": "user",  # Human turn in the chat API.
                "content": prompt,
            },
        ],
    )
    # Alternative: stream=True. Chat Completions stays consistent across Days 01–08 for Ollama compatibility.

    return response.choices[0].message.content.strip()  # First choice text; strip removes stray newlines.
