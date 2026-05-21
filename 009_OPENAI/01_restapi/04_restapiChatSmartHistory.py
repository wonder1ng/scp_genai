# https://developers.openai.com/api/reference/chat-completions/overview
from dotenv import load_dotenv
import requests, os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SYSTEM_PROMPT = "너는 나를 도와주는 20년 경력 작명가야"
message = [{"role": "system", "content": SYSTEM_PROMPT}]
MAX_RECENT_MESSAGES = 10

message.append({"role": "user", "content": user_input})
def call_chatgpt(messages, temperature=1.0):
    # 유저 발언 기억
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": temperature,
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
    )

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

def summarize_conversation(conversation_list):
    """
    기존 대화 요약
    """
    summary_prompt = [
        {
            "role": "system",
            "content": (
                "너는 대화 요약 전문가",
                "사용자와 AI의 대화를 핵심만 간결히 요약해",
                "중요한 요청사항, 취향, 맥락을 유지해"
            )
        },
        {
            "role": "user",
            "content": str(conversation_list)
        }
    ]

    summary = call_chatgpt(summary_prompt, temperature=0.3)

    return summary

def manage_message_history():
    """
    대화가 길어지면 내용을 요약해서
    mesasage[1]에 저장
    """

    actual_conversation_count = len(message) - 1

    if actual_conversation_count > MAX_RECENT_MESSAGES:
        has_summary = len(message) > 1 and message[1]["role"] == "system" and "[대화 요약]" in message[1]["content"]
    
    old_messages = message[1: -MAX_RECENT_MESSAGES]

    if has_summary:
        old_messages.insert(0, message[1])
    
    summary_text = summarize_conversation(old_messages)

    summary_message = {
        "role": "system",
        "content": f"[대화 요약]\n{summary_text}"
    }

    recent_messages = message[-MAX_RECENT_MESSAGES:]

    message = [
        message[0],
        summary_message
    ] + recent_messages

def ask_chatbot(user_input):
    message.append({"role": "user", "content": user_input})
    
    try:
        final_reponse = call_chatgpt(message)
        message.append({"role": "assistant", "content": final_reponse})
        manage_message_history()

        return final_reponse
    except Exception as e:
        return f"오류 발생: {e}"

while True:
    user_input = input("\n당신의 질문: ").strip()
    if user_input.lower() in ["quit", "exit", "종료", "끝"]:
        break
    else:
        print("대화를 생성중입니다. 잠시만 기다려주세요.")
        print("챗봇 응답:", ask_chatbot(user_input))
        print("=" * 60)