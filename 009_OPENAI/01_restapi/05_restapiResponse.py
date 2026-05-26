from dotenv import load_dotenv
import requests, os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

user_input = "대한민국의 수도는 어디야?"

response = requests.post(
    # "https://api.openai.com/v1/chat/completions",
    "https://api.openai.com/v1/responses",
    json={
        "model": "gpt-4o-mini",
        "input": user_input,
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}" # Basic 인증 = Basic Authorization
    }
)

data = response.json()
print(data)
# answer = data["choices"][0]["message"]["content"]
answer = data["output"][0]["content"][0]["text"]
print("=" * 30)
print(answer)
print("응답:", answer)