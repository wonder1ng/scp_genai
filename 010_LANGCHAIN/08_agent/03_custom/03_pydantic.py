import json
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

class SendEmailInput(BaseModel):
    """이메일 전송 도구의 인자"""
    to: str = Field(description="수신자 이메일 주소(반드시 유효한 이메일 형식)")
    subject: str = Field(description="메일 제목(50자 이내 간결하게)")
    body: str = Field(description="메일 본문(반드시 한국어로 작성)")
    priority: Literal["low", "normal", "high"] = Field(default="normal", 
                                                       description="우선순위. urgent한 경우에는 high 사용")

@tool(args_schema=SendEmailInput)
def send_email(to: str, subject: str, body: str, priority: str="normal") -> str:
    """사용자가 요청할 때 이메일을 보냄"""
    print(f"[가짜 전송] to={to}, priority={priority}")
    print(f"제목: {subject}")
    print(f"본문: {body}")
    return f"이메일이 {to}에게 전송되었습니다. (priority={priority})"

class SearchInput(BaseModel):
    """검색 도구의 인자"""
    query: str = Field(description="검색어")
    max_results: int = Field(default=5, ge=1, le=20, description="결과 개수 (1~20)")
    sort_by: Literal["relevance", "date"] = Field(
        default="relevance",
        description="정렬 기준. 최신 정보가 중요하면 date 사용"
    )

@tool(args_schema=SearchInput)
def search(query: str, max_results: int, sort_by: str = "relevance") -> list[str]:
    """주어진 쿼리로 검색 수행"""
    return [f"결과 {i+1}: {query} (정렬={sort_by})" for i in range(max_results)]

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools([send_email, search])

print("=== 도구 명세 ===")
print(json.dumps(send_email.args_schema.model_json_schema(), indent=2, ensure_ascii=False))

print("=== 도구 실제 호출 ===")

questions = [
    "alice@wxample.com에게 회의 일정 변경이라는 제목으로 메일 보내. 본문은 '회의가 내일 3시로 변경되었습니다.'로 보내. 긴급해",
    "파이썬 비동기 프로그래밍 최신 자료 10개만 날짜 순으로 검색해",
    "오늘 점심 메뉴로 샌드위치와 콜라를 주문해"
]

SYSTEM = (
    "도구는 적합할 때만 사용."
    "입력 인자를 잘 확인해서 오류 없도록 호울."
    "호출 이 후 오류가 발생한 경우 도구의 목적과 인자값을 잘 확인해 재시도. 재시도 최대 2회."
    "적합한 도구 미발견 시 '해당 작업을 수행할 수 있는 도구가 없습니다.'라고 답변."
)

for q in questions:
    print(f"\n질문: {q}")
    r = llm_with_tools.invoke([SystemMessage(SYSTEM), HumanMessage(q)])

    if not r.tool_calls:
        print(f"도구 없는 결과: {r.content}")
        break
    for call in r.tool_calls:
        print(f" -> {call['name']} ({call['args']})")

        name2tool = {t.name: t for t in [send_email, search]}
        result = name2tool[call["name"]].invoke(call["args"])
        print(f"결과: {result}")