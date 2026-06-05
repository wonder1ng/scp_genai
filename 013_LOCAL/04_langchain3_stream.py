from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="mistral")

prompt = PromptTemplate.from_template("다음 주제로 작성할만한 블로그 개요를 5가지 만들어.\n\n주제: {topic}")

chain = prompt | llm | StrOutputParser()
chunks = []
for chunk in chain.stream({"topic": "로컬 LLM 모델 활용"}):
    print(chunk, end="", flush=True)
    chunks.append(chunk)
print()
print(len(chunks), len("".join(chunks)))