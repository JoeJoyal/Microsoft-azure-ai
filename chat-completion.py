import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Read Azure configuration
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

# Validate environment variables
if not all([endpoint, deployment_name, api_key]):
    raise ValueError("Missing Azure configuration. Check your .env file.")

# Initialize Azure AI client
client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

# Send chat completion request
completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    temperature=0.3
)

# Print the response
print(completion.to_json)
# print(completion.choices[0].message.content)