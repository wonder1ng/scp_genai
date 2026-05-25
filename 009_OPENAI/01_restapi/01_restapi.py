# https://developers.openai.com/api/reference/chat-completions/overview
from dotenv import load_dotenv
import requests, os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

user_input = "안녕하세요, 반갑습니다."

response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    json={
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Your are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 1.0,
        "top_p": 0.5    # 생성할 단어 확률의 합이 x가 될때까지 후보군 지정
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}" # Basic 인증 = Basic Authorization
    }
)

data = response.json()
final_response = data["choices"][0]["message"]["content"]
print(final_response)