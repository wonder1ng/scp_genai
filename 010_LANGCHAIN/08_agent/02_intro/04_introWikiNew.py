from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import wikipedia

load_dotenv()

wikipedia.wikipedia.USER_AGENT = ("mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) chrome/94.0.4606.61 safari/537.36")

wiki_ko = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(lang="ko", top_k_results=3, doc_content_chars_max=200),
    name="wiki_ko",
    description="한국어 위키피디아. 한국에서 일어난 사건 또는 인물, 개념 등"
)

wiki_en = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(lang="en", top_k_results=3, doc_content_chars_max=200),
    name="wiki_en",
    description="English Wikipedia. 글로벌 / 영어권 주제 또는 한국어 위키 정보가 부족할 때 사용"
)
llm = ChatOpenAI(model="gpt-4o-mini")

system_prompt = """
당신은 위키피디아를 활용해 정보를 조회하고 답변하는 챗봇입니다.
도구 사용 가이드:
- 한국 또는 한국어 관련 주제는 한국어 위키피디어에서 검색
- 글로벌/영어권 주제는 English Wikipedia에서 검색
- 검색 결과가 한번에 안나올 경우, 유사어(유의어) 등으로 변경해서 재시도 할수 있음.

영어 검색한 결과인 경우, 한국어로 번역해서 답변하세요.
"""

agent = create_agent(llm, [wiki_en], system_prompt=system_prompt)

questions = ["what is artificial intelligence?", "세종대왕은 누구인가요?"]
for q in questions:
    try:
        result = agent.invoke({"messages": ["user", q]})
    except Exception as e:
        print(f"[에러] {type(e).__name__}: {e}")
        continue

    print(f"질문: {q}")
    for m in result["messages"]:
        if hasattr(m, "tool_calls") and m.tool_calls:
            for c in m.tool_calls:
                print(f" -> 사용한 도구: {c["name"]} ({c["args"]})")
        if m.type == "tool":
            print(f" <- 결과: {m.content[:100]}...")

    print(f"\n[최종답변] {result["messages"][-1].content}")