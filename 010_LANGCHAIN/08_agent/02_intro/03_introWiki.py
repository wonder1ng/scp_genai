import wikipedia
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI

load_dotenv()

tools = load_tools(["wikipedia"])
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, tools)

result = agent.invoke({"messages": [("user", "인공지능의 역사에 대해 간략히 설명해")]})
print(result)