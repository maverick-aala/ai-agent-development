from openai import OpenAI, APIError
from dotenv import load_dotenv

import os

# load configurations from the .env file
load_dotenv()

#create a cleint that communicates with ollama (AI Model)
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    timeout=120.0
)

print("*"*40)
print("Start Conversation Day 02")
print("*"*40)

messages_history=[]
user_input = input("You: ")


try:
    while user_input != "quit":

        messages_history.append( 
            {
                "role": "user",
                "content": user_input
            }
        )
        #send a question to the AI Model
        response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages_history,
                max_tokens=4096,
                extra_body={
                "options": {
                    "num_predict": 4096,  # Tells Ollama directly to allow long generation
                    "temperature": 0.3    # Lower temperature reduces repeating/hanging loops
                }
            }
        )

        # Safely display the response content
        message_content = response.choices[0].message.content
        if message_content:
            print(message_content)
            messages_history.append({
                "role": "assistant",
                "content": message_content
            })
        else:
            print("Received an empty response from the model.")

        user_input = input("You: ")

except APIError as e:
    print(f"OpenAI API Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

