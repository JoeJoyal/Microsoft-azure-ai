import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2025-01-01-preview"
)

speech = client.audio.speech.create(
    model=os.environ["AZURE_OPENAI_TTS_DEPLOYMENT"],
    voice="alloy",
    input="A golden retriever is generally a friendly and loyal family dog.",
    response_format="wav"
)

speech.write_to_file("dog.wav")
print("Audio saved to dog.wav")