# mamba install chromadb
# mamba install langchain-chroma
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "coding"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def build_store():
    docs = PyPDFLoader(os.path.join(os.path.dirname(__file__), "javascriptSecureCoding.pdf")).load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    store = Chroma.from_documents(
        chunks, embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=DB_DIR
    )
    return store

def load_store():
    store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    print(f"기존 DB 로딩 성공 - {store._collection.count()} 청크 로딩됨")
    return store

def add_store(store: Chroma):
    n = store._collection.count()
    docs = PyPDFLoader(os.path.join(os.path.dirname(__file__), "javascriptSecureCoding.pdf")).load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    store.add_documents(chunks)
    print(f"collection 추가 성공 - {store._collection.count() - n} 청크 추가되어 총 {store._collection.count()} 청크 저장됨")

if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
    store = load_store()
    if store._collection.count() < 500:
        add_store(store)
else:
    store = build_store()

results = store.similarity_search("시큐어코딩이란 무엇인가요?", k=2)
for i, d in enumerate(results, 1):
    print(f"\n\n {i}\t-> {d.page_content[:60]}...")