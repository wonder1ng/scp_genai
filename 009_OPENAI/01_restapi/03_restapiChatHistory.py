# https://developers.openai.com/api/reference/chat-completions/overview
from dotenv import load_dotenv
import requests, os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

message = []
message.append({"role": "system", "content": "너는 나를 도와주는 20년 경력 작명가야"})

def ask_chatbot(user_input):
    # 유저 발언 기억
    message.append({"role": "user", "content": user_input})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": message,
                "temperature": 1.0,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}" # Basic 인증 = Basic Authorization
            }
        )

        data = response.json()
        final_response = data["choices"][0]["message"]["content"]
        # 봇의 발언 기억
        message.append({"role": "assistant", "content": final_response})
        message = [message[0]] + message[-10:]
    except Exception as e:
        print(e)
        
    return final_response

while True:
    user_input = input("\n당신의 질문: ").strip()
    if user_input.lower() in ["quit", "exit", "종료", "끝"]:
        break
    else:
        print("대화를 생성중입니다. 잠시만 기다려주세요.")
        print("챗봇 응답:", ask_chatbot(user_input))
        print("=" * 60)