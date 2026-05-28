from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 브랜드 기획자입니다."),
    ("user", 
     "회사를 홍보하기 위한 캐치프레이즈를 만들어"
     "회사명: {company}"
     "상품명: {product}"
     )
])

filled_prompt = prompt.format(company="테슬라", product="Model S")
print("완성된 프롬프트:", filled_prompt)

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke(filled_prompt)
print(response.content)

from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser

parse1 = StrOutputParser()
parse2 = CommaSeparatedListOutputParser()

result_str = parse1.invoke(response)
result_csv = parse2.invoke(response)

print("문자열 결과:", result_str)
print("CSV 결과:", result_csv)