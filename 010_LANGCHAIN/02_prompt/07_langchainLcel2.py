import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 브랜딩 컨텐츠 기획자입니다."),
    HumanMessagePromptTemplate.from_template("회사를 홍보하기 윈한 {company} 회사의 {product} 상품을 기반으로 캐치프레이즈를 만들어 주세요.")
])

llm = ChatOpenAI(mode="gpt-4o-mini")
parser = StrOutputParser()

# 이 체이닝 문법을 LCEL(LangChaing Expression Language)라고 부름
# chain = prompt | llm | parser | 
chain = prompt | llm | parser | StrOutputParser()
chain = prompt | llm | parser | RunnableLambda(lambda x: {"response": x})

# inputs = {"company": "삼성전자", "product": "메모리"}
inputs = {"company": "하이닉스", "product": "HBM"}
result = chain.invoke(inputs)

print(result)
# 아래 부분도 체인에 포함됨
# final_result = {"response": result}
# print(final_result)

