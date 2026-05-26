from dotenv import load_dotenv
import requests, os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

user_input = "대한민국의 수도는 어디야?"

def chat(user_input, previous_response_id=None):
    req_json={
            "model": "gpt-4o-mini",
            "input": user_input,
        }
    if previous_response_id:
        req_json["previous_response_id"] = previous_response_id
        

    response = requests.post(
        # "https://api.openai.com/v1/chat/completions",
        "https://api.openai.com/v1/responses",
        json=req_json,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}" # Basic 인증 = Basic Authorization
        }
    )

    return response

data = chat(user_input).json()
print(data)
# answer = data["choices"][0]["message"]["content"]
answer = data["output"][0]["content"][0]["text"]
print("=" * 30)
print(answer)
print("응답:", answer)
response_id = data["id"]
print("응답 ID:", response_id)


user_input = "그곳의 대표 관광지 10개 나열"
data = chat(user_input, response_id).json()
print(data)
# answer = data["choices"][0]["message"]["content"]
answer = data["output"][0]["content"][0]["text"]
print("=" * 30)
print(answer)
print("응답:", answer)
response_id = data["id"]
print("응답 ID:", response_id)