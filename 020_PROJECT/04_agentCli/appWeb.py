# 금융 도우미 에이전트 챗봇 만들기

# 랭체인들을 불러온다

from ast import literal_eval

from flask import Flask, request, jsonify, render_template, send_from_directory
from finTools import TOOLS
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
import yfinance as yf
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

checkpoint = MemorySaver()
account = {"KRW": 9000000, "USD": 800.00, "stocks": [{"AAPL": {"name": "APPLE", "shares": 10}}]}

SYSTEM = f"""
당신은 금융 정보 비서 겸 금융 보조 서비스 테스트 AI입니다.
tool의 결과를 참고하여 질문에 적절한 답변을 생성하시오.
환율은 목표 통화가 1일 때를 기준으로 반환하시오.
tool로 해결할 수 없으면 직접 해결하시오.
실제 금융 거래가 이루어진 것처럼 행동하시오.
아래의 경우는 내용에 맞춰 바로 반환하시오.
예약의 경우 {{"reserve": condtion(ex: "AAPL주가 <= USD 150.0 -> 6000주 매수")}}
알림이나 알람의 경우 {{"alarm": condtion(ex: "AAPL주가 == KRW 150.0")}}
"""
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, TOOLS)
agent = create_agent(llm, TOOLS, checkpointer=checkpoint, interrupt_before=["tools"], system_prompt=SYSTEM)
config = {"configurable": {"thread_id": "t001"}}

app = Flask(__name__)

@app.get("/")
def index():
    return send_from_directory("static", "index.html")
    return render_template("index.html")

@app.post("/chat")
def ask():
    global agent
    global checkpoint
    q = request.get_json().get("q")
    print('[질문]', q)
    if q == "1":
        result = agent.invoke(None, config=config)
        final = result["messages"][-1].content
        if not final:
            final = result["messages"][-2].content
        print(f"[최종] {final}")
        if final.startswith("{"):
            final = literal_eval(final)

        return jsonify({"message": final})

    agent = create_agent(llm, TOOLS, checkpointer=checkpoint, interrupt_before=["tools"], system_prompt=SYSTEM)
    checkpoint = MemorySaver()
    
    print("=== 툴 상태 확인 ===")
    for t in TOOLS:
        print(f"[Tool] {t.name}")
        print(f"설명: {t.description}")
        print(f"인자 스키마: {t.args_schema.model_json_schema()}")

    print("\n\n=== 툴 호출 ===")
    result = agent.invoke({"messages": [("user", q)]}, config=config)
    print(f"[질문] {q}")
    ai_msg = agent.get_state(config).values["messages"][-1]
    if ai_msg.tool_calls:
        call = ai_msg.tool_calls[0]
        print(f"[에이전트 제안] {call["name"]} ({call["args"]})")

    for msg in result["messages"]:
        print(f"- {msg.__class__.__name__}: {msg.content}")
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"  └─ 툴 호출 시도: {msg.tool_calls}")

    print(f"\위처럼 진행될 예정입니다. 진행하시겠습니까?")

    return jsonify({"message": "계속 진행하실 거라면 1을, 다른 요청하실 거라면 그 외를 입력하세요."})

@app.post("/reserve")
def reserve():
    pass

@app.post("/alarm")
def alarm():
    pass

@app.post("/approve")
def approve():
    pass

@app.post("/log")
def log():
    pass

if __name__ == "__main__":
    app.run(debug=True)