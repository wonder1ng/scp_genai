import sqlite3
import uuid
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, send_from_directory, session, url_for
import openai, os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SYSTEM_PROMPT = "너는 나를 도와주는 챗봇이야"
MAX_RECENT_MESSAGES = 10
messageGlobal = []

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot.db")
conn = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = "secret"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/uid")
def uid():
    uid = session.get("uid", str(uuid.uuid4()))
    session["uid"] = uid
    global messageGlobal
    messageGlobal = [{"role": "system", "content": SYSTEM_PROMPT}] + list(excute_fetch("select role, content from history where uid = ?", [uid]))
    return jsonify({"uid": uid, "messages": messageGlobal[1:]})

@app.route("/api/chat", methods=["POST"])
def chat():
    uid = session.get("uid")
    global messageGlobal
    if uid:
        data = request.get_json()
        chat_message = data.get("chatMessage", '')
        print("사용자 입력값:", chat_message)
        if len(messageGlobal) > MAX_RECENT_MESSAGES:
            messageGlobal = summary_chatbot(messageGlobal)
        gpt_reply = ask_chatgpt(chat_message)
        cursor.executemany("insert into history (role, content, uid) values (?, ?, ?)", [["user", chat_message, uid], ["bot", gpt_reply, uid]])
        conn.commit()

        messageGlobal += [["user", chat_message], ["bot", gpt_reply]]
        print("messageGlobal")
        print(messageGlobal)

        return jsonify({"reply": f"{gpt_reply}"})
    return redirect(url_for("index"))

@app.route("/api/erase")
def erase():
    cursor.execute("delete from history where uid=?", [session.get("uid")])
    conn.commit()
    return jsonify({"result": "success"}), 200

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

def summary_chatbot(messageGlobal):
    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
        {
            "role": "system",
            "content": 
            """
            너는 대화 요약 전문가
            사용자와 AI의 대화를 핵심만 간결히 요약해
            중요한 요청사항, 취향, 맥락을 유지해
            """
        },
        {
            "role": "user",
            "content": str(messageGlobal[:-MAX_RECENT_MESSAGES])
        }
    ]
    )
    
    print("출력확인:", response)
    messageGlobal = [messageGlobal[0],
                     {"role": "system", "content": f"[대화 요약]\n{response.choices[0].message.content}"}
                     ] + messageGlobal[-MAX_RECENT_MESSAGES:]
    return messageGlobal

def init_db():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        uid TEXT NOT NULL)
        """)
    
def excute_fetch(query, args={}):
    cursor.execute(query, args)
    result = cursor.fetchall()
    return result

if __name__ == "__main__":
    # past_messages = init_db()
    # print(dict(zip([1, 2, 3, 4], past_messages)))
    # [print(e) for e in past_messages]
    # past_messages = []
    # messageGlobal += past_messages
    app.run(debug=True)
    conn.close()