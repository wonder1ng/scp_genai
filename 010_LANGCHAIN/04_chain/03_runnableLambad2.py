from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt_name = ChatPromptTemplate.from_template(
    "{product} 만드는 회사 이름 하나 추천. 이름만 반환"
)
prompt_slogan = ChatPromptTemplate.from_template(
    "{company_name} 회사의 캐치프레이즈 생성. 회사명과 캐치프레이즈만 반환"
)

chain1 = (
    prompt_name | llm | StrOutputParser() | RunnableLambda(lambda name: {"company_name": name.strip()} if print(name) else {"company_name": name.strip()}) | 
    prompt_slogan | llm | StrOutputParser() | RunnableLambda(lambda slogan: {"slogan": slogan.strip()})
)

result1 = chain1.invoke({"product": "친환경 에코백"})
print(f"타입: {type(result1)}")
print(f"결과: {result1}")

chain2 = (
    prompt_name | llm | StrOutputParser() | RunnableLambda(lambda name: {"company_name": name.strip()} if print(name) else {"company_name": name.strip()}) | 
    RunnableLambda(lambda d: {
        "company_name": d["company_name"],
        "slogan": (
            prompt_slogan |
            llm |
            StrOutputParser()
            ).invoke({
                "company_name": d["company_name"]
            })
        })
)

result2 = chain2.invoke({"product": "친환경 에코백"})
print(f"타입: {type(result2)}")
print(f"결과: {result2}")