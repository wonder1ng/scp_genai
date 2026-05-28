from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

MODEL = "gpt-4o-mini"

llm = ChatOpenAI(model=MODEL)


app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/name")
def name():
    prompt = [
        SystemMessage("You are a creative creative brand expert"),
        HumanMessage("Waht's a good company name that makes computer games. do not give any explanation. just give me the company names"),
    ]
    result = llm.invoke(prompt)

    return jsonify({"result": "success", "chatbot": result.content})

@app.route("/api/name", methods=["POST"])
def name2():
    data = request.get_json()
    product = data.get("product")
    user_prompt = f"Waht's a good company name that makes {product}. do not give any explanation. just give me the company names"
    prompt = [
        SystemMessage("You are a creative creative brand expert"),
        HumanMessage(user_prompt),
    ]
    result = llm.invoke(prompt)

    return jsonify({"result": "success", "chatbot": result.content.split("\n")})

@app.route("/api/dinner")
def dinner():
    prompt = [
        SystemMessage("당신은 경력 10년차 호텔 훼프입니다."),
        HumanMessage("오늘 저녁 메뉴를 추천해줘"),
    ]
    result = llm.invoke(prompt)
    print(result.content)
    print("result.content_blocks")
    print(result.content_blocks)

    return jsonify({"result": "success", "chatbot": result.content_blocks})

if __name__ == "__main__":
    app.run(debug=True)
