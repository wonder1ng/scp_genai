from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

research_prompt = ChatPromptTemplate.from_template(
    "다음 주제에 대해 핵심 사실 5가지를 간결히 정리해\n\n주제: {topic}"
)

research_chain = research_prompt | llm | parser

gate_prompt = ChatPromptTemplate.from_template(
    """
    다음 리서치 결과가 적합한지 평가해
    리서치 결과: {research}
    평가 기준:
    1. 사실 5가지가 올바르게 포함됐는가?
    2. 각 사실이 구체적이고 검증 가능한가?
    3. 주제와 관련이 있는가?
    결과: PASS or FAIL로만 대답하고 PASS인 경우 `PASS`만 반환, FAIL인 경우 이유를 한줄로 설명
    """
)
gate_chain = gate_prompt | llm | parser

analysis_prompt = ChatPromptTemplate.from_template(
    """
    다음 리서치 결과를 바탕으로 심층 분석 내용을 작성
    리서치 결과: {research}
    다음을 포함해
    - 핵심 트렌드 또는 패턴
    - 시사점
    - 향후 전망
    """
)

analysis_chain = gate_prompt | llm | parser

report_prompt = ChatPromptTemplate.from_template(
    """
    다음 리서치와 분석된 내용을 바탕으로 CEO에게 보고할 간결한 보고서 작성
    리서치: {research}
    분석: {analysis}
    출력 형식:
    - 제목
    - 요약 (3줄)
    - 핵심 발견사항
    - 결론
    """
)

report_chain = report_prompt | llm | parser

def run_chaining_pipeline(topic):
    print("[1단계] 리서치 수행 중")
    research = research_chain.invoke({"topic": topic})

    print("[2단계] 게이트 검증 수행 중")
    gate_result = gate_chain.invoke({"research": research})
    print("2단계 결과", gate_result)
    if "fail" in gate_result.lower():
        gate_result = gate_chain.invoke({"research": research})
    
    print("[3단계] 분석 수행 중")
    analysis = analysis_chain.invoke({"research": research})

    print("[4단계] 보고서 생성 수행 중")
    report = report_chain.invoke({"research": research, "analysis": analysis})

    return report

topic = "2026년도 생성형 AI 시장 동향 조사를 해오시오."

result = run_chaining_pipeline(topic)
print("=" * 20)
print("최종보고서:")
print("=" * 20)

print(result)