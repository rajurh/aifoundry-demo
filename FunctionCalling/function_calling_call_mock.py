import json
import os

import azure.identity
import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
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
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "gpt-4o")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


def lookup_weather(city_name=None, zip_code=None):
    """Lookup the weather for a given city name or zip code."""
    print(f"Looking up weather for {city_name or zip_code}...")
    return "It's sunny!"


def lookup_stock_price(symbol=None):
    """Mock stock price lookup."""
    print(f"Looking up stock price for {symbol}...")
    return f"The current price of {symbol} is $123.45."


tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_weather",
            "description": "Lookup the weather for a given city name or zip code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "The city name",
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "The zip code",
                    },
                },
                "strict": True,
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_stock_price",
            "description": "Lookup the current stock price for a given company symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock ticker symbol, e.g., AAPL for Apple.",
                    },
                },
                "strict": True,
                "additionalProperties": False,
            },
        },
    }
]

messages = [
    {"role": "system", "content": "You are an AI assistant that can answer weather and stock price questions."},
    {"role": "user", "content": "What's the weather in Berkeley and the stock price for AAPL?"},
]

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

print(f"Response from {MODEL_NAME} on {API_HOST}: \n")

# Handle tool call(s)
if response.choices[0].message.tool_calls:
    tool_calls = response.choices[0].message.tool_calls
    function_messages = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        if function_name == "lookup_weather":
            function_result = lookup_weather(**arguments)
        elif function_name == "lookup_stock_price":
            function_result = lookup_stock_price(**arguments)
        else:
            function_result = "Function not implemented."
        function_messages.append({
            "role": "function",
            "name": function_name,
            "content": function_result,
        })
    followup_messages = messages + function_messages
    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=followup_messages,
    )
    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)