"""
Day 06 — Same as Day 05 chat loop; uses CHAT_MODEL in .env (separate from EMBEDDING_MODEL for retrieval labs).
"""

import os  # Read BASE_URL, API_KEY, and model names from os.environ after load_dotenv().
import re  # Detect filename-like .txt tokens in the user message (Day 05–06).
from openai import OpenAI, APIError
# APIError: SDK exception for API/HTTP failures. Alternative: httpx.HTTPStatusError with raw HTTP.
# We use the OpenAI SDK: Ollama and many hosts expose an OpenAI-compatible API (same code locally and in the cloud).

from dotenv import load_dotenv
# Alternative: export variables in the shell; `.env` keeps secrets out of source code.

from util import get_user_choice
from tools import get_current_time, read_text_file

# Load key/value pairs from `.env` in the working directory into os.environ.
load_dotenv()

# HTTP client for the language model — points at Ollama or another OpenAI-compatible server (not always api.openai.com).
client = OpenAI(
    base_url=os.getenv("BASE_URL"),  # Often http://localhost:11434/v1 for Ollama.
    api_key=os.getenv("API_KEY"),  # Any placeholder for local Ollama; real key for OpenAI cloud — keep in .env.
    timeout=120.0,  # Seconds before the client aborts; local models can be slow on cold start.
)
# Alternative: `OpenAI()` with no base_url (OpenAI cloud only). Alternative: AsyncOpenAI for async servers.

print("*" * 50)
print("Start Conversation Day 06 ", get_current_time())
print("*" * 50)

choice = get_user_choice()
messages_history = [
    {
        "role": "system",  # Persona/instructions that steer all following replies (Day 03+).
        "content": choice,
    }
]
user_input = input("\nYou: ")


def alter_user_input(local_user_input):
    """If message references a .txt file, substitute file contents for the path (Day 05–06)."""
    if ".txt" in local_user_input.lower():
        match = re.search(r"[a-zA-Z0-9-_\.\/\\]+\.txt", local_user_input)
        if match:
            filename = match.group(0)
            file_content = read_text_file(filename)
            local_user_input = re.sub(
                r"[a-zA-Z0-9-_\.\/\\]+\.txt", file_content, local_user_input
            ).strip()
            return local_user_input
    return local_user_input


try:
    while user_input.lower() != "quit":

        updated_user_input = alter_user_input(user_input.strip("'\""))

        messages_history.append(
            {
                "role": "user",  # Human turn in the chat API.
                "content": updated_user_input,
            }
        )

        response = client.chat.completions.create(
            model=os.getenv("CHAT_MODEL"),  # Chat model from .env (Day 06+; separate from EMBEDDING_MODEL).
            messages=messages_history,
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
        if message_content:
            print("\nAI: ", message_content)
            messages_history.append(
                {
                    "role": "assistant",  # Model reply kept in history for the next turn.
                    "content": message_content,
                }
            )
        else:
            print("Received an empty response from the model.")

        user_input = input("\nYou: ")

except APIError as e:
    print(f"OpenAI API Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
