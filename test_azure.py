from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/"
)

print("Endpoint:", os.environ["AZURE_OPENAI_ENDPOINT"])
print("Deployment:", os.environ["AZURE_OPENAI_DEPLOYMENT"])

response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "user", "content": "Say hello in one sentence."}
    ],
    max_tokens=50
)

print(response.choices[0].message.content)