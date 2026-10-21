import os
from openai import OpenAI
from dotenv import load_dotenv

# load configurations from the .env file
load_dotenv()

#create a cleint that communicates with ollama (AI Model)
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

#send a question to the AI Model
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "user",
            "content": "What is Artificial Intelligence?"
        }
    ]
)

#dispplay the response
print(response.choices[0].message.content)