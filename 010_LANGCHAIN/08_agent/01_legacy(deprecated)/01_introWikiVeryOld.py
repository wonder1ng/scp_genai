# # mamba install wikipedia
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_community.agent_toolkits.load_tools import load_tools
# from langchain.agents import initialize_agent, AgentType

# load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini")

# tools = load_tools(["wikipedia"])

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# result = agent.invoke({"input": "인공지능의 역사에 대해 간략히 설명해"})
# print(result["output"])

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.agent_toolkits.load_tools import load_tools

load_dotenv()

# LLM
model = ChatOpenAI(model="gpt-4o-mini")

# Agent (LangChain v1 권장 방식)
agent = create_agent(
    model=model,
    tools=load_tools(["wikipedia"]),
    system_prompt="당신은 유용한 AI 비서입니다."
)

# 실행
result = agent.invoke({"messages": [{"role": "user",
                                     "content": "인공지능의 역사에 대해 간략히 설명해"}]
                                     })
print(result["messages"][-1].content)