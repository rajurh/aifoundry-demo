"""
This script demonstrates how to use Azure AI Projects and Azure OpenAI to:
- Run a chat completion using a techno punk persona
- Evaluate the response using the Azure AI Evaluation SDK

Configuration is managed via environment variables in the .env file.
"""

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

# Load environment variables from .env file, overriding any existing ones
load_dotenv(override=True)

# Get the Azure AI Project endpoint from the environment or use a fallback
endpoint = os.environ.get("AIPROJECT_ENDPOINT", "https://ai-foundry-demo1.services.ai.azure.com/api/projects/firstProject")

# Instantiate the AIProjectClient for project operations
project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)

# Get a chat inferencing client using the project's default model inferencing endpoint
chat = project.inference.get_chat_completions_client()

query = "Hey, can you help me with my taxes? I'm a freelancer."
# Run a chat completion using the inferencing client and persona prompt
chat_model = os.environ.get("CHAT_MODEL", "gpt-4o")
response = chat.complete(
    model=chat_model,
    messages=[
        {"role": "system", "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?"},
        {"role": "user", "content": query},
    ]
)

content = response.choices[0].message.content
print("Response: ", content)

# Evaluate the response using Azure AI Evaluation SDK
from azure.ai.evaluation import RelevanceEvaluator

try:
    # Try to get the default Azure OpenAI connection (with credentials)
    connection = project.connections.get_default(
        connection_type=ConnectionType.AZURE_OPEN_AI,
        include_credentials=True)
except ValueError as e:
    print("No default AZURE_OPEN_AI connection found. Please configure one in your Azure AI Project.")
    connection = None

if connection:
    # Build the evaluator model config from environment variables
    evaluator_model = {
        "azure_endpoint": os.environ.get("EVALUATION_AZURE_ENDPOINT"),
        "azure_deployment": os.environ.get("EVALUATION_MODEL", "gpt-4.1-mini"),
        "api_version": os.environ.get("EVALUATION_API_VERSION", "2025-01-01-preview"),
        "api_key": os.environ.get("EVALUATION_API_KEY"),
    }

    # Run the relevance evaluation
    relevance = RelevanceEvaluator(evaluator_model)
    score = relevance(query=query, response=response)
    print(score)