from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

docs = [
    Document(page_content="NVMe는 SSD의 인터페이스 규격으로 PCIe를 사용한다."),
    Document(page_content="SATA SSD는 NVMe보다속도가 느리다."),
    Document(page_content="HDD는 회전 디스크 기반이라 IO가 느린 편이다."),
    Document(page_content="ㅍ이썬은 인기 있는 프로그래밍 언어다."),
    Document(page_content="자바스크립트는 부라우저에서 동작하는 언어다."),
    Document(page_content="Rust는 메모리 안정성과 성능을 동시에 추구한다."),
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
retriever = store.as_retriever(search_kwargs={"k": 2})

prompt = ChatPromptTemplate.from_template(
"""
아래의 문서를 참고하여 질문에 답하시오.\n\n
문서:\n{context}
질문:\n{question}
"""
)

def format_docs(docs: []) -> str:
    """검색된 Document 리스트를 하나의 문자열로 변환"""
    return "\n\n".join(d.page_content for d in docs)

chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# question = "NVMe와 SATA의 차이는 무엇인가요?"
question = "파이썬은 어떤 언어인가요?"
print(f"사용자 질문: {question}")
print(f"답변: {chain.invoke(question)}")