from dotenv import load_dotenv
import requests, os, csv
from google import genai

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="나는 한국에 살고 있는 20대 개발자야. 저메추"
)

print(response.text)