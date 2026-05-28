from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

load_dotenv()

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 SQL 전문가입니다. 순수하게 SQL 쿼리문만으로 답변하고 아무런 사족 달지 마세요."),
    ("human", "DB Schema: \n{schema}\n\nUser Query: {query}"),
])

schema = """
Table: users
 - id (INTEGER)
 - name (TEXT)
 - email (TEXT)
 - signup_date (DATE)

Table: orders
 - id (INTEGER)
 - user_id (INTEGER)
 - product_name (TEXT)
 - price (INTEGER)
 - created_at (DATE)"""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = chat_prompt | llm | RunnableLambda(lambda x: {"sql": x.content.strip()})

questions = [
    "2023년 1월 1일 이후 가입한 사용자의 이름과 이메일을 조회해",
    "주문 금액이 5만 원 이상인 주문 목록 조회",
    "사용자 별 총 주문 금액 계산",
    "가장 최근 주문한 사람과 그 상품명 5개 반환",
    "회원 가입 후 한번도 주문하지 않은 사람 조회"
]

for idx, question in enumerate(questions, start=1):
    print("=" * 30)
    print(f"질문 {idx}, {question}")
    result = chain.invoke({"schema": schema, "query": question})
    print(f"\n생성된 SQL:\n{result["sql"]}")