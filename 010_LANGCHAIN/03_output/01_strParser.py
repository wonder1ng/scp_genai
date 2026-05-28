from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser

load_dotenv()

prompt1 = ChatPromptTemplate.from_template(
    "{product} 회사 이름 하나 추천"
)

llm = ChatOpenAI(model="gpt-4o-mini")

chain1 = prompt1 | llm | StrOutputParser()
result1 = chain1.invoke({"product": "웹게임"})

print(f"타입: {type(result1)}")
print(f"결과: {result1}")

prompt2 = ChatPromptTemplate.from_template(
    "{topic} 관련 키워드 5개 쉼표로 구분해서 나열"
)
chain2 = prompt2 | llm | CommaSeparatedListOutputParser()
result2 = chain2.invoke({"topic": "인공지능"})

print(f"타입: {type(result2)}")
print(f"결과: {result2}")

prompt_name = ChatPromptTemplate.from_template(
    "{product} 만드는 회사 이름 하나 추천. 이름만 반환"
)
prompt_slogan = ChatPromptTemplate.from_template(
    "{company_name} 회사의 캐치프레이즈 생성. 회사명과 캐치프레이즈만 반환"
)

chain3 = (
    prompt_name | llm | StrOutputParser() | (lambda name: {"company_name": name.strip()} if print(name) else {"company_name": name.strip()}) | 
    prompt_slogan | llm | StrOutputParser()
)

result3 = chain3.invoke({"product": "친환경 에코백"})
print(f"타입: {type(result3)}")
print(f"결과: {result3}")