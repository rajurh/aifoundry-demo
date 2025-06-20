import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv(override=True)

# Configure OpenAI for Azure (v1+ SDK)
client = openai.AzureOpenAI(
    api_key=os.environ.get("EVALUATION_API_KEY"),
    api_version=os.environ.get("EVALUATION_API_VERSION", "2025-01-01-preview"),
    azure_endpoint=os.environ.get("EVALUATION_AZURE_ENDPOINT"),
)

# Example chat completion call (v1+ SDK)
response_aoai = client.chat.completions.create(
    model=os.environ.get("EVALUATION_MODEL", "gpt-4.1-mini"),
    messages=[
        {"role": "system", "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?"},
        {"role": "user", "content": "Hey, can you help me with my taxes? I'm a freelancer."},
    ],
    stream=True
)

print("\n🗨️  Azure OpenAI Response:")
for chunk in response_aoai:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
