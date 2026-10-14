
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2025-01-01-preview"
)

# Open the audio file
with open("counting-fast.wav", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model=os.environ["AZURE_OPENAI_WHISPER_DEPLOYMENT"],
        file=audio_file,
        response_format="text"
    )

print("Transcribed text:")
print(transcription)
