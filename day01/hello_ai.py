"""
Day 01 — Minimal first call to a chat model via an OpenAI-compatible HTTP API (e.g. Ollama).
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

response = client.chat.completions.create(
    model=os.getenv("MODEL"),  # Model name from .env (Ollama tag or OpenAI model id).
    messages=[
        {
            "role": "user",  # Human turn in the chat API.
            "content": "What is Artificial Intelligence?",
        }
    ],
)
# Single-turn call (no history yet — Day 02 adds messages_history). Alternative: stream=True for streaming output.

print(response.choices[0].message.content)  # First choice text; may be None if output is empty.
