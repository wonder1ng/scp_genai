import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
full_path = lambda path: os.path.join(os.path.dirname(__file__), path)

client = OpenAI()

def transcribe_audio(file):
    with open(file, "rb") as af:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=af,
            response_format="text",
            language="ko"
        )
    return transcript

result = transcribe_audio(full_path("harvard.wav"))
print("결과:", result)