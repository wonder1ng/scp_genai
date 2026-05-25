from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
import openai, os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder="static", static_url_path="")

history = []

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    chat_message = data.get("chatMessage", '')
    print("사용자 입력값:", chat_message)

    history.append({"role": "user", "conent": chat_message})
    gpt_reply = ask_chatgpt(chat_message)
    history.append({"role": "assistant", "content": gpt_reply})

    return jsonify({"reply": f"{gpt_reply}"})

def ask_chatgpt(chat_message):
    gpt_ask_message = [
        {"role": "system", "content": "당신은 친절하지만 평생을 경상도에서 살아 경상도 사투리 내이티브인 장년의 남성입니다."},
        history
    ]

    print("="*30)
    print("우리가 물어볼 메세지:", gpt_ask_message)
    print("="*30)

    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=gpt_ask_message
    )
    print("출력확인:", response)
    return response.choices[0].message.content  

if __name__ == "__main__":
    app.run(debug=True)