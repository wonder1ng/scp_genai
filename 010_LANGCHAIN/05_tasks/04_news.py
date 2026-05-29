from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnableParallel

# 목적 - 뉴스를 분석한다.
# 뉴스 입력 -> 요약 
#          -> 감정분석 
#          -> 카테고리 분석
# RunnableParallel

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

base_prompt = ChatPromptTemplate(
    [("system", "다음 기사에 대해 {action} 기술하시오"),
     ("human", "{text}")])

chain_summary = base_prompt.partial(action="3줄 요약하여 간략히") | llm | RunnableLambda(lambda x: x.content.strip())
chain_analysis = base_prompt.partial(action="감정 분석하여 어떤 감정인지 간략히") | llm | RunnableLambda(lambda x: x.content.strip())
chain_categorize = base_prompt.partial(action="어떤 카테고리의 기사인지 분석하여 간략히") | llm | RunnableLambda(lambda x: x.content.strip())

input_text = {
    "text": """자율형 AI 에이전트 마누스(Manus AI)의 연간 구독료가 한국 구글 플레이 스토어에서 96% 할인된 가격에 노출되는 글리치가 5월 11일경부터 발생했다. 평소 약 24만 원대(연 199달러 안팎)에 형성되던 마누스 Pro 연 구독이 한국 안드로이드 계정에서만 약 3만 2,000원/연으로 표시됐고, 이 사실이 한국 IT 커뮤니티 사이에서 빠르게 확산되며 결제 행렬이 이어졌다. 이른바 '마누스 대란'이다.\n마누스는 싱가포르에 본사를 둔 버터플라이 이펙트(Butterfly Effect)가 만든 자율형 AI 에이전트로, 사용자 명령 한 줄에 웹 검색·문서 작성·코드 실행·예약을 스스로 처리하는 도구다. 2025년 3월 초대 코드 한정 베타로 출발해 시연 영상이 하루 만에 100만 뷰를 넘기며 폭발적 관심을 모았고, 8개월 만에 연환산 매출(ARR) 1억 달러를 돌파했다.\n글로벌 대기자 명단은 50만 명을 넘긴 상태였다. 5월 14일 현재 일부 사용자는 결제 직후 계정 차단 사례를 보고하고 있고, 마누스 측은 환불 정책만 안내한 채 사건 자체에 대한 공식 입장을 내놓지 않고 있다.\n무엇이 잘못됐나\n마누스 Pro의 정상 가격은 월 20달러(연 환산 약 200달러대), 같은 등급의 챗GPT(ChatGPT) Plus·클로드(Claude) Pro와 비슷한 수준이다. 그런데 한국 구글 플레이에 노출된 가격은 약 1/8 수준이었다. 사용자들 사이에서는 '환율·지역 가격 정책 적용 실수', '안드로이드 빌링 콘솔 설정 오류', '연 단위 가격과 월 단위 가격을 혼동한 토큰 오류' 등의 추정이 돌았다. 글로벌 SaaS는 보통 구글 플레이 콘솔에서 국가별 현지화 가격을 설정하는데, 그 단계에서 0이 한 자리 빠지거나 통화 단위가 잘못 적용되면 정확히 이런 글리치가 발생한다. 같은 가격이 iOS·웹·다른 국가의 안드로이드에서는 노출되지 않았으며 한국 안드로이드 사용자에게만 발생한 것으로 보인다.\n'일단 사고 보자' — 결제 폭주 후 일부 계정 블록\n가격 표기가 사실인지 확신할 수 없는 상태에서도 사용자들은 '일단 결제부터' 움직였다. 인공지능 에이전트 도구 1년치를 매우 저렴한 가격에 구매할 수 있다는 기대가 작용하면서 카드 결제 한도를 채우거나 여러 계정으로 동시 결제를 시도한 사례도 나왔다. 그러나 결제 직후 일부 사용자 계정에서 즉각적인 차단·접속 오류가 발생했다는 보고가 이어졌다. 결제는 정상 처리됐지만 구독 활성화가 되지 않거나 인증 오류 메시지가 뜨는 경우가 있었다.\n마누스 측은 공식 헬프센터를 통해 멤버십 환불 절차와 크레딧 환불 정책을 안내하고 있다. 자체 정책에는 버그나 플랫폼 오작동에 대한 자동 크레딧 환불이 포함돼 있으며, 안드로이드 결제의 경우 구글 플레이 정책에 따라 일정 기간 내 환불 또는 개발자 직접 환불 절차를 따른다.\n마누스 측 대응의 핵심 변수 — '오류 가격 인정' vs '서비스 유지'\n이번 사건의 시나리오는 크게 두 가지로 나뉜다. 하나는 오류 가격을 인정하고 기존 결제를 유지하는 경우이고, 다른 하나는 일괄 환불 및 구독 취소 처리다. 일반적으로 글로벌 SaaS에서는 후자가 더 흔하지만 사용자 반발 가능성이 크다. 과거 여러 플랫폼에서도 가격 오류 발생 시 자동 환불로 정리된 사례가 많다. 다만 마누스는 모회사 관련 구조 변화와 거버넌스 이슈가 겹쳐 있어 의사결정이 복잡한 상황이다. 또한 외부 투자 및 인수 관련 갈등 속에서 조직 재편이 진행 중이라는 점도 변수로 작용한다.\n시사점 — 한국 시장에서의 첫 'AI 결제 사고'\n이번 사건은 한국 시장에서 글로벌 AI 에이전트 서비스의 첫 대규모 결제 오류 사례로 기록될 가능성이 크다. 한국 사용자가 주요 시장 중 하나로 부상하고 있는 상황에서 글로벌 SaaS 가격 정책 오류가 실제 결제로 이어질 수 있다는 점이 드러났다. 향후 환불 처리 결과에 따라 소비자 보호 이슈 및 플랫폼 책임 논의로 확산될 가능성도 있다."""
}

parallel_chain = RunnableParallel({
    "summary": chain_summary,
    "analysis": chain_analysis,
    "categorize": chain_categorize,
})

result = parallel_chain.invoke(input_text)
[print(k + "\n" + result[k]) for k in result.keys()]