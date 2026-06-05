# 금융 도우미 에이전트 챗봇 만들기

# 랭체인들을 불러온다

from finTools import TOOLS
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
import yfinance as yf
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()

SYSTEM = """
당신은 금융 정보 비서입니다.
tool의 결과를 참고하여 질문에 적절한 답변을 생성하시오.
tool로 해결할 수 없으면 해당되는 tool이 없다고 답변하시오.
환율은 목표 통화가 1일 때를 기준으로 반환하시오.
"""
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, TOOLS, system_prompt=SYSTEM)
def ask(q):
    # agent를 통해서 해당 질문을 호출한다.
    print('[질문]', q)

    print("=== 툴 상태 확인 ===")
    for t in TOOLS:
        print(f"[Tool] {t.name}")
        print(f"설명: {t.description}")
        print(f"인자 스키마: {t.args_schema.model_json_schema()}")

    print("\n\n=== 툴 호출 ===")

    result = agent.invoke({"messages": [("user", q)]})
    agent.invoke()
    print(f"[질문] {q}")
    # for call in r.tool_calls:
    #     print(f" -> {call["name"]} ({call["args"]})")

    #     result = name2tool[call["name"]].invoke(call["args"])
    #     print(f" -> 결과: {result}")
    #     print(r)
    
    for msg in result["messages"]:
        print(f"- {msg.__class__.__name__}: {msg.content}")
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"  └─ 툴 호출 시도: {msg.tool_calls}")
    final_answer = result["messages"][-1].content
    print(f"\n[최종 LLM 응답 메시지]\n{final_answer}")

if __name__ == "__main__":
    print('=== 데모 명령어 실행 ===')
    for q in ["삼성전자 주가 알려줘", "달러 환율 얼마야?", "엔비디아 관련 최근 뉴스는 뭐가 있어?"]:
    # for q in ["달러 환율 얼마야?", "엔비디아 관련 최근 뉴스는 뭐가 있어?", "로보롭란 기업에 대해 알려줘"]:
        ask(q)
        input("\n 일시 정지 \n")

    print('=== 수동 질의 응답 시작 ===')
    while True:
        # 사용자로부터 질문을 받아서 'q', 'quit', 'exit', 가 올때까지 반복한다.

        if not q or q.lower() in ("q", "quit", "exit", "ㅂ"):
            break