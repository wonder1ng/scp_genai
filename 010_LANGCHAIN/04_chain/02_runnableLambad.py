from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

class MovieReview(BaseModel):
    """영화 리뷰 분석 결과"""
    title: str = Field(description="영화 제목")
    sentiment: str = Field(description="감성 분류: 긍정, 부정, 중립")
    score: int = Field(description="1~10 점수")
    summary: str = Field(description="리뷰 요약 (1~2문장)")
    keywords: list[str] = Field(description="핵심 키워드 3개")

llm = ChatOpenAI(model="gpt-4o-mini")

parser = PydanticOutputParser(pydantic_object=MovieReview)
print("포멧 명령문:")
print(parser.get_format_instructions())

prompt = ChatPromptTemplate.from_template(
    """다음 영화 리뷰 분석 요청
    리뷰: {review}

    {format_instructions}"""
)

chain = prompt | llm | parser

reviews = [
    "영화 클레멘타인: 당신이 이 영화를 보지 않았다면 아직 살아있을 이유 하나를 간직하고 있는 것이다. (별점 10)",
    "영화 성냥팔이소녀의 재림: 이것은절대1점이아니다11점을주고싶은 내마음이다. (별점 1)",
    "영화 다세포소녀: 박평식 인터스텔라 7점, 다크나이트 7점, 다세포소녀 6점.영화평론가라는게 얼마나 쓰잘데없는 직업인지 알게된다ㅋㅋㅋ (별점 10)"
]

for review in reviews:
    result = chain.invoke({
        "review": review,
        "format_instructions": parser.get_format_instructions()
    })

    print(f"제목: {result.title}")
    print(f"감성: {result.sentiment} (점수: {result.score}/10)")
    print(f"요약: {result.summary}")
    print(f"키워드: {result.keywords}")
    print("=" * 30)

# 제목: 클레멘타인
# 감성: 긍정 (점수: 9/10)
# 요약: 영화를 보지 않은 사람은 아직 살아있을 이유를 간직하고 있다.
# 키워드: ['클레멘타인', '영화', '살아있다']
# ==============================
# 제목: 성냥팔이소녀의 재림
# 감성: 긍정 (점수: 11/10)
# 요약: 영화 '성냥팔이소녀의 재림'에 대한 강한 긍정적인 반응이 느껴지며, 점수는 극한의 11점이다.
# 키워드: ['성냥팔이소녀', '재림', '강력한추천']
# ==============================
# 제목: 다세포소녀
# 감성: 부정 (점수: 6/10)
# 요약: 영화 평론가의 평가가 의문스러운 리뷰입니다. 영화 다세포소녀는 평균 이하의 점수를 받았다고 언급하고 있습니다.
# 키워드: ['영화 평론', '다세포소녀', '점수']
# ==============================

# 제목: 클레멘타인
# 감성: 긍정 (점수: 10/10)
# 요약: 이 영화는 관객에게 강력한 감정을 불러일으키며, 삶의 의미에 대한 깊은 통찰을 제공합니다. 꼭 보아야 할 작품입니다.
# 키워드: ['클레멘타인', '영화', '추천']
# ==============================
# 제목: 성냥팔이소녀의 재림
# 감성: 부정 (점수: 1/10)
# 요약: 영화에 대한 강한 실망감이 표현된 리뷰입니다. 리뷰어는 1점을 주었지만 실제로는 11점을 주고 싶다는 감정을 드러내고 있습니다.
# 키워드: ['실망', '재림', '감정']
# ==============================
# 제목: 다세포소녀
# 감성: 부정 (점수: 6/10)
# 요약: 영화 평론가의 평가는 신뢰할 수 없고, 영화에 대한 비판이 다소 유머러스하게 표현되었다.
# 키워드: ['다세포소녀', '영화 평론가', '별점']
# ==============================