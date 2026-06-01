# 표준 LCEL로 RAGE 모델 구현
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()
full_path = lambda filename: os.path.join(os.path.dirname(__file__), filename)
DB_DIR = full_path("chroma_db")
COLLECTION_NAME = "my_rag"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

store = Chroma(collection_name=COLLECTION_NAME,
               embedding_function=embeddings,
               persist_directory=DB_DIR)

if store._collection.count() == 0:
    docs = TextLoader(full_path("nvme.txt"), encoding="utf_8").load() + TextLoader(full_path("hbm.txt"), encoding="utf_8").load()

    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    for c in chunks:
        c.metadata["source"] = os.path.basename(c.metadata.get("source", "?"))
    
    store.add_documents(chunks)

retriever = store.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 문서 기반 QA시스템입니다. 아래 문서만 참고해서 답변하시오.\n문서:\n{context}"),
    ("user", "{question}")
])

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

chain = (
    RunnablePassthrough.assign(context=lambda x: print(format_docs(retriever.invoke(x["question"]))) or format_docs(retriever.invoke(x["question"])))
    | prompt
    | llm
    |StrOutputParser()
)

print(chain.invoke({"question": "NVMe와 HBM의 차이"}))