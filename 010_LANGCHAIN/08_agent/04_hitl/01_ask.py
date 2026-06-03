# 휴먼 인 더 루프(HITL, Human-in-the-Loop)
# 인공지능(AI)이나 자동화 시스템이 작업을 수행하는 과정에
# 인간이 직접 개입하여 감독, 검토, 피드백을 제공하는 협업 방식
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

checkpoint = MemorySaver()

@tool
def send_payment(recipient: str, amount: int) -> str:
    """수신자에게 지정 금액을 송금"""
    return f"{recipient}에게 {amount}원 송금 완료"

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [send_payment], checkpointer=checkpoint, interrupt_before=["tools"])

config = {"configurable": {"thread_id": "t001"}}

question = "홍길동에게 10,000원 송금해"

print(f"[유저] {question}")
result = agent.invoke({"messages": [("user", question)]}, config=config)

call = result["messages"][-1].tool_calls[0]
print(f"[일시정지] {call["name"]} ({call["args"]})")

human_result = input("\n이대로 실행할까요? (y/n)").strip().lower()
if human_result == "y":
    result = agent.invoke(None, config=config)
    print(f"[최종결론] {result["messages"][-1].content}")
else:
    print(f"\n[중단] 사용자 요청에 의해 중단되었습니다.")