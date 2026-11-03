"""
Day 07 — Planner picks a local tool; Python runs it; LLM formats the answer (two chat completion calls).
"""

import os  # Read BASE_URL, API_KEY, and model names from os.environ after load_dotenv().

from openai import OpenAI
# Alternative: `import ollama` — Ollama-only. Alternative: raw HTTP (`httpx`) — more boilerplate.
# We use the OpenAI SDK: Ollama and many hosts expose an OpenAI-compatible API (same code locally and in the cloud).

from dotenv import load_dotenv
# Alternative: export variables in the shell; `.env` keeps secrets out of source code.

from planner import choose_tools
from tools import get_current_time, roll_dice, generate_password

# Load key/value pairs from `.env` in the working directory into os.environ.
load_dotenv()

# HTTP client for the language model — points at Ollama or another OpenAI-compatible server (not always api.openai.com).
client = OpenAI(
    base_url=os.getenv("BASE_URL"),  # Often http://localhost:11434/v1 for Ollama.
    api_key=os.getenv("API_KEY"),  # Any placeholder for local Ollama; real key for OpenAI cloud — keep in .env.
)
# Alternative: `OpenAI()` with no base_url (OpenAI cloud only). Alternative: AsyncOpenAI for async servers.

print("~" * 40)
print(" My AI Agent")
print("~" * 40)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "quit":
        print("\nAI: Goodbye! Have a great day.")
        break

    tool = choose_tools(user_input)

    if tool == "get_current_time":
        result = get_current_time()
    elif tool == "roll_dice":
        result = roll_dice()
    elif tool == "generate_password":
        result = generate_password()
    else:
        result = None

    prompt = f"""
    The user asked: {user_input}

    The tool returned: {result}

    Answer the user naturally. Don't mentioned anything related to tool. if tool is returning none then check if you can answer by yourself.
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

    print("\nAI: ", response.choices[0].message.content)  # First choice text; may be None if output is empty.
