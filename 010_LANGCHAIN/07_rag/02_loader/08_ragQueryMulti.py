# mamba install chromadb
# mamba install langchain-chroma
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()
def path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)
DB_DIR = path("chroma_db")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def load_store(collection_name: str) -> Chroma:
    store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    print(f"기존 DB 로딩 성공 - {store._collection.count()} 청크 로딩됨" if store._collection.count() else f"새로운 {collection_name} collection 생성됨")
    return store

def save_store(store: Chroma, filename: str) -> None:
    n = store._collection.count()
    if ".txt" in filename:
        docs = TextLoader(path(filename), encoding="utf_8").load()
    elif ".pdf" in filename:
        docs = PyPDFLoader(path(filename)).load()
    else:
        print(f".txt나 .pdf파일만 가능합니다. {filename}은 추가되지 못했습니다.")
        return
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    store.add_documents(chunks)
    print(f"collection 추가 성공 - {store._collection.count() - n} 청크 추가되어 총 {store._collection.count()} 청크 저장됨")

retrievers = []
for f in ["hbm.txt", "nvme.txt", "javascriptSecureCoding.pdf"]:
    store = load_store(f.split(".")[0])
    if not store._collection.count():
        save_store(store, f)
    retrievers.append(store.as_retriever(search_kwargs={"k": 2}))

def multi_retrieve(question):
    return "\n\n".join("\n\n".join(d.page_content for d in r.invoke(question)) for r in retrievers)
    
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 문서 기반 Q&A 시스템입니다.아래 문서만을 참고해서 답하고 문서에 적합한 내용이 없으면 '모른다'라고 답변하세요.\n\n문서:\n{context}"),
    ("user", "{question}")
])


chain = (
    RunnablePassthrough.assign(context=lambda x: multi_retrieve(x["question"]))
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke({"question": "HBM이란 무엇인가요?"}))
print("=" * 30)
print(chain.invoke({"question": "NVMe와 HBM은 다른건가요?"}))