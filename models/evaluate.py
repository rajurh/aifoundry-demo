from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Use the endpoint directly from the .env or fallback to a hardcoded value
endpoint = os.environ.get("AIPROJECT_ENDPOINT", "https://ai-foundry-demo1.services.ai.azure.com/api/projects/firstProject")

project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)

# get a chat inferencing client using the project's default model inferencing endpoint
chat = project.inference.get_chat_completions_client()

query = "Hey, can you help me with my taxes? I'm a freelancer."
# run a chat completion using the inferencing client
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

# Evaluate the response
from azure.ai.evaluation import RelevanceEvaluator

try:
    connection = project.connections.get_default(
        connection_type=ConnectionType.AZURE_OPEN_AI,
        include_credentials=True)
except ValueError as e:
    print("No default AZURE_OPEN_AI connection found. Please configure one in your Azure AI Project.")
    connection = None

if connection:
    evaluator_model = {
        "azure_endpoint":"https://demoazureopenai1223.openai.azure.com/", #connection.endpoint_url,
        "azure_deployment": "gpt-4.1-mini", #os.environ.get("EVALUATION_MODEL", "gpt-4.1-mini"),
        "api_version": "2025-01-01-preview",
        "api_key": "Replace", #connection.key,
    }

    relevance = RelevanceEvaluator(evaluator_model)
    score = relevance(query=query, response=response)
    print(score)