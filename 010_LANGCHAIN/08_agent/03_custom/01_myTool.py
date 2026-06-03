from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

@tool
def claculator(expression: str) -> str:
    """수학식을 계산. 예: 53 * 7 + 2"""
    try:
        # 예외처리를 해 LLM의 오입력으로부터 실행 유치
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"계산 오류: {e}"

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [claculator])

result = agent.invoke({
    # "messages": [("user", "10 니누기 2 곱하기 5는?")]
    "messages": [("user", "10 니누기 2 곱하기 5는?")]
})

print("최종답변:", result["messages"][-1].content)