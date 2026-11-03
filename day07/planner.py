"""
Day 07 — LLM planner: map user text to a local tool name (or none).
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


def choose_tools(user_request):
    planner_prompt = f"""
    You are an AI Planner.

    Available tools:
    1. get_current_time: Use this tool when user ask for current time or latest time.
    2. roll_dice: Use this tool when user ask to roll a dice.
    3. generate_password: Use this tool when user wants a secure password.
    4. None: if no tool is required then return

    return ONLY the tool name.

    user_request: {user_request}
    """

    response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),  # Chat model from .env (Day 06+; separate from EMBEDDING_MODEL).
        messages=[
            {
                "role": "system",  # Persona/instructions that steer all following replies (Day 03+).
                "content": "You are an AI planner",
            },
            {
                "role": "user",  # Human turn in the chat API.
                "content": planner_prompt,
            },
        ],
    )
    # Alternative: stream=True. Chat Completions stays consistent across Days 01–08 for Ollama compatibility.

    return response.choices[0].message.content  # First choice text; may be None if output is empty.
