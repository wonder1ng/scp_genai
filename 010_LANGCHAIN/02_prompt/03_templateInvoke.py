from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 작명가입니다."),
    ("user", "다음 상품을 만드는 회사의 이름을 지어주세요. 상품명: {product}")
])

filled_prompt = prompt.format(product="자율주행 자동차")
print("완성된 프롬프트:", filled_prompt)

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke(filled_prompt)
print(response.content)