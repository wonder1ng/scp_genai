from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, send_from_directory, session, url_for
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel, RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

pormpt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 한국어 어시스턴트입니다."),
    MessagesPlaceholder("history"),
    ("user", "{input}")
])

chain = pormpt | llm | StrOutputParser()

sessions: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in sessions:
        sessions[session_id] = InMemoryChatMessageHistory()
    return sessions[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

def chatting(message, session_id):
    print(f"\n[{session_id}] 질문: {message}")
    answer = chain_with_memory.invoke(
        {"input": message},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"[{session_id}] 답변: {answer}")
    return answer

app = Flask(__name__)
app.secret_key= "chat secret"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    message = request.get_json().get("message")
    print(message)
    return jsonify({"result": "success", "message": chatting(message, session.get("user"))})

@app.route("/api/login")
def login():
    if request.args.get("user"):
        session["user"] = request.args.get("user")
    return jsonify({"result": "success", "user": session.get("user")})

@app.route("/api/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)