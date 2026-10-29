from openai import OpenAI
from dotenv import load_dotenv
import os

from planner import choose_tools
from tools import (get_current_time, roll_dice, generate_password)

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("~"*40)
print(" My AI Agent")
print("~"*40)

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
        model=os.getenv("CHAT_MODEL"),
        messages=[{
            "role":"user",
            "content": prompt
        }]
    )

    print("\nAI: ", response.choices[0].message.content)



