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

connection = project.connections.get_default(
    connection_type=ConnectionType.AZURE_OPEN_AI,
    with_credentials=True)

evaluator_model = {
    "azure_endpoint": connection.endpoint_url,
    "azure_deployment": os.environ.get("EVALUATION_MODEL", "gpt-4o-mini"),
    "api_version": "2024-06-01",
    "api_key": connection.key,
}

relevance = RelevanceEvaluator(evaluator_model)
score = relevance(query=query, response=response)
print(score)