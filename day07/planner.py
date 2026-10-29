from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

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
        model=os.getenv("CHAT_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI planner"
            },
            {
                "role": "user",
                "content": planner_prompt
            }
        ]
    )

    # print(response.choices)
    return response.choices[0].message.content