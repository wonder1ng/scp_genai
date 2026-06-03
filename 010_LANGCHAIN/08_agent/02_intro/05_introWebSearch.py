from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
# TavilySearch: 구글 검색을 쉽게 만들어 줌
# 구글 API로 직접 구현해도 됨
# pip install langchain-tavily
# conda는 버전이 낮은데 관련 패키지를 엄청 옛날 걸로 다운그레이드 해서 사용 하면 안 됨

load_dotenv()

web_search = TavilySearch(max_results=3)
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [web_search])

result = agent.invoke({"messages": [("user", "LnagChain의 최신 버전은?")]})
print(result["messages"][-1].content)