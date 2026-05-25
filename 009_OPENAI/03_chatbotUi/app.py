from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
import openai, os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder="static", static_url_path="")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    chat_message = data.get("chatMessage", '')
    print("사용자 입력값:", chat_message)
    gpt_reply = ask_chatgpt(chat_message)
    return jsonify({"reply": f"{gpt_reply}"})

def ask_chatgpt(chat_message):
    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Your are a helpful assistant."},
                {"role": "user", "content": chat_message}
            ]
    )
    print("출력확인:", response)
    return response.choices[0].message.content  

if __name__ == "__main__":
    app.run(debug=True)