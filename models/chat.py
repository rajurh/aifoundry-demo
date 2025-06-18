import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv(override=True)

endpoint = os.environ.get("AIPROJECT_ENDPOINT", "https://ai-foundry-demo1.services.ai.azure.com/api/projects/firstProject")
chat_model = os.environ.get("CHAT_MODEL", "gpt-4o")

project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)

# get a chat inferencing client using the project's default model inferencing endpoint
chat = project.inference.get_chat_completions_client()

# run a chat completion using the inferencing client
response = chat.complete(
    model=chat_model,
    messages=[
        {"role": "system", "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?"},
        {"role": "user", "content": "Hey, can you help me with my taxes? I'm a freelancer."},
    ],
    stream=True
)

# print chunks as they become available
print("🗨️  Response:")
for event in response:
    if event.choices:
        print(event.choices[0].delta.content, end="", flush=True)