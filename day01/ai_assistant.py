"""
Day 01 — Interactive REPL: repeated user questions until "quit", with basic error handling.
"""

import os  # Read BASE_URL, API_KEY, and model names from os.environ after load_dotenv().

from openai import OpenAI, APIError
# APIError: SDK exception for API/HTTP failures. Alternative: httpx.HTTPStatusError with raw HTTP.
# We use the OpenAI SDK: Ollama and many hosts expose an OpenAI-compatible API (same code locally and in the cloud).

from dotenv import load_dotenv
# Alternative: export variables in the shell; `.env` keeps secrets out of source code.

# Load key/value pairs from `.env` in the working directory into os.environ.
load_dotenv()

# HTTP client for the language model — points at Ollama or another OpenAI-compatible server (not always api.openai.com).
client = OpenAI(
    base_url=os.getenv("BASE_URL"),  # Often http://localhost:11434/v1 for Ollama.
    api_key=os.getenv("API_KEY"),  # Any placeholder for local Ollama; real key for OpenAI cloud — keep in .env.
    timeout=120.0,  # Seconds before the client aborts; local models can be slow on cold start.
)
# Alternative: `OpenAI()` with no base_url (OpenAI cloud only). Alternative: AsyncOpenAI for async servers.

print("*" * 40)
print("Start Conversation Day 01")
print("*" * 40)

user_input = input("You: ")

try:
    while user_input != "quit":  # Exit when user types quit (case-sensitive; Day 03+ uses .lower()).

        response = client.chat.completions.create(
            model=os.getenv("MODEL"),  # Model name from .env (Ollama tag or OpenAI model id).
            messages=[
                {
                    "role": "user",  # Human turn in the chat API.
                    "content": user_input,  # Day 01: only this turn — no messages_history yet (Day 02+).
                }
            ],
            max_tokens=4096,  # Max completion tokens (honored by OpenAI-compatible servers).
            extra_body={
                "options": {
                    "num_predict": 4096,  # Ollama max output tokens (mirrors max_tokens).
                    "temperature": 0.3,  # Lower = less random; reduces rambling on small local models.
                }
            },
        )
        # Alternative: stream=True. Chat Completions stays consistent across Days 01–08 for Ollama compatibility.

        message_content = response.choices[0].message.content  # First choice text; may be None if output is empty.
        print("Response Choices: ", response)
        if message_content:
            print(message_content)
        else:
            print("Received an empty response from the model.")

        user_input = input("You: ")

except APIError as e:
    print(f"OpenAI API Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
