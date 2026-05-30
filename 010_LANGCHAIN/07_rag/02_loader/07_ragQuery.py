# mamba install chromadb
# mamba install langchain-chroma
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "coding"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def build_store():
    docs = TextLoader(os.path.join(os.path.dirname(__file__), "nvme.txt"), encoding="utf_8").load()
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
    docs = TextLoader(os.path.join(os.path.dirname(__file__), "nvme.txt"), encoding="utf_8").load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    store.add_documents(chunks)
    print(f"collection 추가 성공 - {store._collection.count() - n} 청크 추가되어 총 {store._collection.count()} 청크 저장됨")

if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
    store = load_store()
    if store._collection.count() < 520:
        add_store(store)
else:
    store = build_store()

results = store.similarity_search("HBM이란 무엇인가요?", k=2)

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 문서 기반 Q&A 시스템입니다.아래 문서만을 참고해서 답하고 문서에 적합한 내용이 없으면 '모른다'라고 답변하세요.\n\n문서:\n{context}"),
    ("user", "{question}")
])

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

retriever = store.as_retriever(search_kwargs={"k": 2})

chain = (
    RunnablePassthrough.assign(context=lambda x: format_docs(retriever.invoke(x["question"])))
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke({"question": "HBM의 성능은 어떤가요?"}))
print("=" * 30)
print(chain.invoke({"question": "NVMe와 HBM은 다른건가요?"}))