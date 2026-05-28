from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate

# 목적 - 질문 유형에 따라 적합한 항목으로 답변한다
# 질문 유형 -> 배송조회 상담원
#          -> 결제관련 상담원
#          -> 기술지원 상담원
# RunnableBranch

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

def make_chain(role):
    return (
        ChatPromptTemplate.from_messages([
            ("system", f"역할극입니다. 당신은 {role} 상담원입니다. 당신이 누군지 밝히고 간략히 2문장 내로 답변하세요."),
            ("user", "{question}")
        ]) |
        llm |
        StrOutputParser()
    )
chains = []
for v in ["배송조회", "결제관련", "기술지원", "만능"]:
    chains.append(
        RunnableLambda(lambda x, role = v: print(role) or x)
        | make_chain(v)
        )

branch = RunnableBranch(
    (lambda x: "배송" in x["question"], chains[0]),
    (lambda x: "결제" in x["question"], chains[1]),
    (lambda x: "기술" in x["question"], chains[2]),
    chains[3],
)
questions = [
    "배송 언제 오나요?",
    "결제한 거 환불 받고 싶어요.",
    "vscode에서 notebook 커널이 자꾸 죽는데 기술지원해줘요.",
    "이혜정의 비빔밥 레시피 코드 알려줘"
]

for q in questions:
    print("질문:", q)
    print("답변:", branch.invoke({"question": q}))
    print("="*30)