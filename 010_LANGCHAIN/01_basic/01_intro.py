import os
from dotenv import load_dotenv
# from langchain.llms import OpenAI # 구버전
from langchain.agents import create_agent   # 현재 langchin은 통합 버전
from langchain_openai import OpenAI # 신버전

load_dotenv()
# vscode에서는 .env를 알아서 불러온다.

MODEL = "gpt-4o-mini"
# langchain은 환경 변수에서 "OPENAI_API_KEY" or "OPENAI_ADMIN_KEY" 등 지정되 키값을 알아서 읽음
llm = OpenAI(model=MODEL)
# llm = OpenAI(model=MODEL, api_key=os.getenv("OPENAI_API_KEY"))
print(llm)

prompt = "오늘 저녁은 무엇을 먹을까요?"
result = llm.invoke(prompt)
print(result)

# langchain,agents 버전
agent = create_agent(
    model=MODEL,
    system_prompt="You are a helpful assistant",
    # tools=function
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": prompt}]}
)
print("langchain")
print(result)
print(result["messages"][-1].content_blocks)