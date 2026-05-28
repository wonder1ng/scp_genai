from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

load_dotenv()

examples = [
    {"sentence": "오늘 정말 최고의 하루였어!", "result": "감정: 긍정 / 점수: 9"},
    {"sentence": "이거 진짜 별로네. 시간 낭비", "result": "감정: 부정 / 점수: 10"},
    {"sentence": "평범. 특색 없음", "result": "감정: 중립 / 점수: 1"},
    {"sentence": "와 진짜 감동이에요. 눈물 날 정도였어요.", "result": "감정: 긍정 / 점수: 0"},
    {"sentence": "기대한 만큼은 아니지만 괜찮았음", "result": "감정: 중립 / 점수: 8"},
]

example_prompt = PromptTemplate(
    input_variables=["sentence", "result"],
    template="문장: {sentence}\n분석: {result}"
)

fewshot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="다음은 문장의 감정을 분석한 예시입니다.\n같은  형식으로 다음 문장을 분석하세요.\n\n- 예시 시작",
    suffix="\n예시 종료 -\n- 새로 분석할 문장\n문장: {sentence}\n분석:",
    example_separator="\n-----\n"
)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 한국어 감정 분석기입니다. 예시와 같은 형태로 답변하세요."),
    ("user", "{fewshot_text}")
])

llm = ChatOpenAI(model="gpt-4o-mini")
chain = chat_prompt | llm | StrOutputParser()

target = "오랫만에 만난 친구랑 좋은 시간을 보냈어요. 다음에 또 보고 싶네요."
fewshot_text = fewshot_prompt.format(sentence=target)
result = chain.invoke({"fewshot_text": fewshot_text})
print(result)
print(chain.invoke({"fewshot_text": fewshot_prompt.format(sentence="오랫만에 만난 친구와 좋은 시간 보냄. 추후 재회 희망")}))

print("-----")
plain_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "당신은 한국어 감정 분석기입니다."),
        ("user", "다음 문장의 감정을 분석하세요: {sentence}")
    ])
    | llm
    | StrOutputParser()
)
print(plain_chain.invoke({"sentence": target}))