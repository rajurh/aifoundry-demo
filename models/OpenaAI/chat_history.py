"""
chat_history.py

This script provides a command-line chat interface that maintains conversation history with an LLM (Azure OpenAI, OpenAI.com, Ollama, or GitHub-hosted models).
- The assistant is set up as a Python teaching assistant for Berkeley CS 61A.
- The script supports multi-turn conversations, preserving all previous messages.
- The LLM provider and model are selected via environment variables.
"""

import os

import azure.identity
import openai
from dotenv import load_dotenv

# Load environment variables and select API host
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

# Setup the OpenAI client for the selected provider
if API_HOST == "azure":
    # Azure OpenAI with Azure AD authentication
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_DEPLOYMENT"]
elif API_HOST == "ollama":
    # Ollama local model
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]
elif API_HOST == "github":
    # GitHub-hosted model via Inference API
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "gpt-4o")
else:
    # OpenAI.com
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]

# Initialize the conversation history with a system prompt
messages = [
    {"role": "system", "content": "I am a travel assistant helping in guiding you with top tourist spots in various cities. I will provide concise and informative responses."},
]

# Main chat loop: prompt user, send question, append to history, and print answer
while True:
    question = input("\nYour question: ")
    print("Sending question...")

    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=1,
        max_tokens=400,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    bot_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_response})

    print("Answer: ")
    print(bot_response)