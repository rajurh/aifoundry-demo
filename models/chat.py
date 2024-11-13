from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_connection_string = "eastus2.api.azureml.ms;597966d1-829f-417e-9950-8189061ec09c;rg-dantaylo-e2e-demo2;dantaylo-e2e-demo2"

project = AIProjectClient.from_connection_string(
    conn_str=project_connection_string,
    credential=DefaultAzureCredential()
)

# get a chat inferencing client using the project's default model inferencing endpoint
chat = project.inference.get_chat_completions_client()

# run a chat completion using the inferencing client
response = chat.complete(
    model="phi-3.5-mini-instruct",
    messages=[
        {"role": "system", "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?"},
        {"role": "user", "content": "Hey, can you help me with my taxes? I'm a freelancer."},
    ]
)

print(response.choices[0].message.content)