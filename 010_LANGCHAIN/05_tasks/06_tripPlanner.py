from ast import literal_eval

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

# 목적 - 여행 계획을 작성한다.
# 도시 입력 -> 음식 추천 
#          -> 관광지 추천
#          -> 호텔 추천
# 사용자 입력의 OO을 보고, 시간표/동선/교통수단 vs 음식/관광지/호텔
# RunnableParallel, RunnableBranch

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

if_prompt = ChatPromptTemplate(
    [("system",
      """
      다음의 여행 관련 질문을 보고 반드시 아래 형식의 dict만 반환해.

      {{'result': True, 'city': 'seoul', "text": str}}

      규칙:
      1. result는 여행 계획이 도시의 음식이나 관광지, 숙소 등을 정하는 등 어느 정도 구체적이면 True
      2. 여행 계획이 너무 추상적이면 False
      3. city는 반드시 문자열이어야 함
      4. city는 절대 빈 문자열('', null, None)로 반환하면 안 됨
      5. 질문에 도시가 없으면 가장 적절한 여행 도시를 하나 추천해서 넣어
      6. 반환은 dict 하나만 하고 다른 설명은 절대 추가하지 마
      7. text는 사용자 질문을 그대로 반환해
      8. result와 city, text는 항상 포함해야 함
      """),
     ("human", "{text}")])

true_prompt = ChatPromptTemplate(
    [("system", "당신은 {city}의 30년차 관광 현지 가이드. 관광객에게 {city}의 관광 시 추천할 {obj}에 대해 간략히 작성하시오."),
     ("human", "{text}")])

false_prompt = ChatPromptTemplate(
    [("system", "당신은 {city}의 30년차 현지인. 관광객에게 {city}의 {obj}에 대해 간략히 추천하시오. 다른 여행지는 언급말고 {city}에 대해서만 기술하시오."),
     ("human", "{text}")])

base_chain = if_prompt | llm | RunnableLambda(lambda x: print("\n\n- start", x, sep="\n\n") or literal_eval(x.content))
chains = []
for v in ["시간표", "동선", "교통수단"]:
    chains.append(RunnableLambda(lambda x, obj = v: print(obj) or x) | true_prompt.partial(obj=v) | llm | StrOutputParser())
true_chain = RunnableParallel({
    "timeTable": chains[0],
    "route": chains[1],
    "transport": chains[2],
})
for v in ["음식", "관광지", "호텔"]:
    chains.append(RunnableLambda(lambda x, obj = v: print(obj) or x) | false_prompt.partial(obj=v) | llm | StrOutputParser())
false_chain = RunnableParallel({
    "food": chains[3],
    "attraction": chains[4],
    "hotel": chains[5],
})
branch = base_chain | RunnableBranch((lambda x: x["result"], true_chain), false_chain)

questions = [
    {"text": "한국에서 2박3일로 갔다오기 좋은 해외 여행지. 여유롭게 쉬다 오고 싶어"},
    {"text": "피렌체에서 티본 스테이크와 트러플 파스타를 먹고 성당, 미술관, 박물관, 광장을 관람할 거야"}
]

for q in questions:
    print("질문:", q)
    result = branch.invoke({"text": q})
    print("답변:")
    [print(k + "\n" + result[k] + "\n") for k in result.keys()]
    print("="*30)