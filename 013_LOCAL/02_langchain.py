from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral")

resp = llm.invoke("안녕? 한마디로 너를 간단히 소개해")
print(resp.content)