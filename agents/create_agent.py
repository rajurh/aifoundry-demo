import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FileSearchTool

from dotenv import load_dotenv
load_dotenv()

project = AIProjectClient.from_connection_string(
    conn_str=os.environ['AIPROJECT_CONNECTION_STRING'],
    credential=DefaultAzureCredential()
)

file = project.agents.upload_file_and_poll(file_path="product_info_1.md", purpose="assistants") 
vector_store = project.agents.create_vector_store_and_poll(file_ids=[file.id], name="my_vectorstore") 
file_search = FileSearchTool(vector_store_ids=[vector_store.id]) 

# Create agent with file search tool and process the agent run 
agent = project.agents.create_agent( 
    model="gpt-4o-mini", 
    name="file-search-agent", 
    instructions="Hello, you are helpful agent and can search information from uploaded files", 
    tools=file_search.definitions, 
    tool_resources=file_search.resources, 
)