import os
import re
from openai import OpenAI, APIError
from dotenv import load_dotenv

# custom methods
from util import get_user_choice
from tools import get_current_time, read_text_file

# load configurations from the .env file
load_dotenv()

#create a cleint that communicates with ollama (AI Model)
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    timeout=120.0
)

print("*"*50)
print("Start Conversation Day 06 ", get_current_time())
print("*"*50)

# here role = system is telling AI Model to behave like, for example behave like teacher, developer, parents etc 

choice = get_user_choice()
messages_history=[{
    "role": "system",
    "content": choice
}]
user_input = input("\nYou: ")

def alter_user_input(local_user_input):
    if ".txt" in local_user_input.lower():
        # print("User Input: ",local_user_input)
        match = re.search(r"[a-zA-Z0-9-_\.\/\\]+\.txt", local_user_input)
        if match:
            filename = match.group(0)
            # print("Filename: ",filename)
            file_content = read_text_file(filename)
            
            # replacing filename with filecontent so AI Model can have filecontent
            local_user_input = re.sub(r"[a-zA-Z0-9-_\.\/\\]+\.txt", file_content, local_user_input).strip()
            
            # print(local_user_input)
            return local_user_input
    
    return local_user_input

# Now here we can see that that we have reached to the place where we know what are the limitations of our project, what if multiple files is there is there, what if a file contain lots of data, so now how we will resolve these problems

try:
    while user_input.lower() != "quit":

        # checking if filename is present 
        updated_user_input = alter_user_input(user_input.strip("'\" "))
             
        messages_history.append( 
            {
                "role": "user",
                "content": updated_user_input
            }
        )
        #send a question to the AI Model
        response = client.chat.completions.create(
                model=os.getenv("CHAT_MODEL"),
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
            print("\nAI: ", message_content)
            messages_history.append({
                "role": "assistant",
                "content": message_content
            })
        else:
            print("Received an empty response from the model.")

        user_input = input("\nYou: ")

except APIError as e:
    print(f"OpenAI API Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

