from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="mistral")

prompt = PromptTemplate.from_template("다음 주제로 작성할만한 블로그 개요를 5가지 만들어.\n\n주제: {topic}")

chain = prompt | llm | StrOutputParser()

resp = chain.invoke("안녕? 한마니로 너를 간단히 소개해")
print("resp")
print(resp)
print("resp.content")
print(resp.content)