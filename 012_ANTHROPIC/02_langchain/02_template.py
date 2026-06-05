from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-6")

# PromptTemplate: 단일 답변
template = PromptTemplate.from_template("다음 주제에 대해 간결히 설명해: {topic}")

formatted_prompt = template.format(topic="llm 기술")
response = llm.invoke(formatted_prompt)
print("response")
print(response)
print("response.content")
print(response.content)

# ChatPromptTemplate: 채팅 기반. role 구분
chat_template = ChatPromptTemplate.from_messages([
    ("system", "당신은 {role} 전문가입니다. 질문에 자세히 답변하세요."),
    ("human", "다음 개념에 대해서 설명해주세요: {concept}")
])
chain = chat_template | llm

response = chain.invoke({"role": "인공지능", "concept": "트랜스포머"})
print("response")
print(response)
print("response.content")
print(response.content)
