"""
Day 06 — Embedding API via the same OpenAI-compatible client (embeddings.create, not chat).
"""

import os  # Read BASE_URL, API_KEY, and model names from os.environ after load_dotenv().

from openai import OpenAI
# Alternative: `import ollama` — Ollama-only. Alternative: raw HTTP (`httpx`) — more boilerplate.
# We use the OpenAI SDK: Ollama and many hosts expose an OpenAI-compatible API (same code locally and in the cloud).

from dotenv import load_dotenv
# Alternative: export variables in the shell; `.env` keeps secrets out of source code.

from similarity import cosine_similarity

# Load key/value pairs from `.env` in the working directory into os.environ.
load_dotenv()

# HTTP client for the language model — points at Ollama or another OpenAI-compatible server (not always api.openai.com).
client = OpenAI(
    base_url=os.getenv("BASE_URL"),  # Often http://localhost:11434/v1 for Ollama.
    api_key=os.getenv("API_KEY"),  # Any placeholder for local Ollama; real key for OpenAI cloud — keep in .env.
)
# Alternative: `OpenAI()` with no base_url (OpenAI cloud only). Alternative: AsyncOpenAI for async servers.


def get_embedding_vector(question, content):
    """Return (question_embedding, content_embedding) using EMBEDDING_MODEL from .env."""
    question_embedding = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),  # Embedding model from .env (not CHAT_MODEL).
        input=question,
    ).data[0].embedding

    content_embedding = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=content,
    ).data[0].embedding

    return question_embedding, content_embedding


response1 = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
    input="Python",
)

response2 = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
    input="Language",
)

embedding1 = response1.data[0].embedding
embedding2 = response2.data[0].embedding
