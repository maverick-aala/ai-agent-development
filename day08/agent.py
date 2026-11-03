from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

from model_context_protocol.mcp_client import (
    connect, 
    disconnect, 
    discover_tools, 
    execute_tool
)

#load configuration
load_dotenv()

#create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

async def main():
    client = await connect()

    tools = await discover_tools(
        client
    )

    print("~"*40)
    print("Available Tools")
    print("~"*40)

    for tool in tools:
        print(tool.name)

    # tool_description = build_tool_descriptions(tools)

    user_request = input("User: ")
    
    tool_name = planner(user_request, tools)
    print("Tool name: ", tool_name)

    tool_result = await execute_tool(client, tool_name)
    print("Tool Result: ", tool_result)

    final_answer = generate_response(user_request, tool_result)
    print()
    print("AI: ", final_answer)
    print()

    await disconnect(client)

def build_tool_descriptions(tools):
    descriptions = ""
    for tool in tools:
       descriptions += f"""Tool: {tool.name} Description: {tool.description}"""

    return descriptions

def planner(user_request, tools):
    tool_descriptions = build_tool_descriptions(tools)
    prompt = f"""
                You are an AI Planner.
                Available Tools
                {tool_descriptions}
                Instruction
                1. Select the best tool.
                2. Reply ONLY with the tool name without keyword "Tool:"
                3. Do not explain.

                User Request: {user_request}
            """
    response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    tool_name = response.choices[0].message.content
    return tool_name.strip()

def generate_response(user_request, tool_result):
    prompt = f"""
                The User asked: {user_request}
                The tool returned: {tool_result}
                If user question is related to tool then include that in response and Answer in natural language
            """
    response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    return response.choices[0].message.content

# Checks wheather this file is being run directly.
if __name__ == "__main__":
    #Starts the main asynchronous function. in simple words "If I run this file, start my main program."
    asyncio.run(main())