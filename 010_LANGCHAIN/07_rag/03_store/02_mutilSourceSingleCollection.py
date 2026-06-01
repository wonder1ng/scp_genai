import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()
def full_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)
DB_DIR = full_path("chroma_db")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

FILES = [
    "nvme.txt",
    "hbm.txt",
    "cisc2024.pdf",
]

def load_any_docs(path):
    if path.lower().endswith(".pdf"):
        return PyPDFLoader(path).load()
    else:
        return TextLoader(path, encoding="utf_8").load()

def build_document():
    chunks = []
    for path in FILES:
        part = splitter.split_documents(load_any_docs(full_path(path)))
        for c in part:
            c.metadata["source"] = os.path.basename(path)
            # metadata 넣음
        chunks += part
    
    return Chroma.from_documents(chunks, 
                                 embeddings, 
                                 collection_name="unified", 
                                 persist_directory=DB_DIR)

store = Chroma(collection_name="unified", 
                    embedding_function=embeddings, 
                    persist_directory=DB_DIR)
if store._collection.count() == 0:
    store = build_document()

print(f"컬렉션 이름: inified, 청크 통합 개수: {store._collection.count()}")

# 쿼리
query = "저장장치 인터페이스 속도는?"
for d in store.similarity_search(query, k=1):
    print(f"\n---\n[{d.metadata.get("source")}] {d.page_content}")
    
query = "가장 값싸고 가성비 좋은 패스트푸드는?"
for d in store.similarity_search(query, k=1):
    print(f"\n---\n[{d.metadata.get("source")}] {d.page_content}")

# 메타데이터 키 기반 필터링
results = store.similarity_search(query, k=2, filter={"source": "hbm.txt"})
for d in results:
    print(f"\n---\n{d.page_content}")