"""
Day 02 (extended) — Chat memory plus parsing <think> blocks from reasoning models.
"""

import os  # Read BASE_URL, API_KEY, and model names from os.environ after load_dotenv().
import re  # Split <think> blocks from the user-visible answer.
from dotenv import load_dotenv
# Alternative: export variables in the shell; `.env` keeps secrets out of source code.

from openai import OpenAI, APIError
# APIError: SDK exception for API/HTTP failures. Alternative: httpx.HTTPStatusError with raw HTTP.
# We use the OpenAI SDK: Ollama and many hosts expose an OpenAI-compatible API (same code locally and in the cloud).

# Load key/value pairs from `.env` in the working directory into os.environ.
load_dotenv()

# HTTP client for the language model — points at Ollama or another OpenAI-compatible server (not always api.openai.com).
client = OpenAI(
    base_url=os.getenv("BASE_URL"),  # Often http://localhost:11434/v1 for Ollama.
    api_key=os.getenv("API_KEY"),  # Any placeholder for local Ollama; real key for OpenAI cloud — keep in .env.
    timeout=180.0,  # Longer timeout for reasoning models (default chat scripts use 120.0).
)
# Alternative: `OpenAI()` with no base_url (OpenAI cloud only). Alternative: AsyncOpenAI for async servers.

print("*" * 40)
print("Start Conversation Day 02")
print("*" * 40)

messages_history = []  # List of {role, content} turns — sent on every request for conversation memory (Day 02+).
user_input = input("You: ")


def parse_thinking_and_content(full_content):
    """Return (thinking_text, answer_text) when <think> tags are present."""
    if not full_content:
        return "", ""

    think_match = re.search(
        r"<think>(.*?)</think>", full_content, re.DOTALL | re.IGNORECASE
    )

    if think_match:
        thinking_process = think_match.group(1).strip()
        final_answer = re.sub(
            r"<think>.*?</think>", "", full_content, flags=re.DOTALL | re.IGNORECASE
        ).strip()
        return thinking_process, final_answer
    else:
        return "", full_content.strip()


try:
    while user_input != "quit":
        messages_history.append({"role": "user", "content": user_input})  # Human turn in the chat API.

        print("\nAI is thinking...", end="\r")

        response = client.chat.completions.create(
            model=os.getenv("MODEL"),  # Model name from .env (Ollama tag or OpenAI model id).
            messages=messages_history,
            max_tokens=8192,  # Larger budget so thinking + answer fit (reasoning models only).
            extra_body={
                "options": {
                    "num_predict": 8192,  # Ollama max output tokens (mirrors max_tokens here).
                    "temperature": 0.3,  # Lower = less random; reduces rambling on small local models.
                }
            },
        )
        # Alternative: stream=True. Chat Completions stays consistent across Days 01–08 for Ollama compatibility.

        message_content = response.choices[0].message.content  # First choice text; may be None if output is empty.

        if message_content:
            thinking, answer = parse_thinking_and_content(message_content)

            if thinking:
                print("\n" + "=" * 10 + " 🧠 MODEL THINKING PROCESS " + "=" * 10)
                print(thinking)
                print("=" * 45 + "\n")

            print(f"AI: {answer}")

            messages_history.append(
                {"role": "assistant", "content": message_content}
            )  # Store full raw reply (including <think> tags) for model context.

        else:
            print(
                "\nReceived an empty response from the model. (Try increasing"
                " max_tokens / num_predict further)"
            )

        print("\n" + "-" * 40)
        user_input = input("You: ")

except APIError as e:
    print(f"\nOpenAI API Error: {e}")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
