from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

load_dotenv()


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

query = "NVMe와 SATA의 차이는 무엇인가요?"
results = store.similarity_search(query=query, k=3)

print(f"질문: {query}")
print(f"가장 가까운 {len(results)}개의 문서")
for i, doc in enumerate(results, 1):
    print(f" {i}. {doc.page_content}")