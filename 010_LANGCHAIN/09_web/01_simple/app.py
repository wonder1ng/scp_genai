import io, os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from pypdf import PdfReader

# 랭체인 기본 불러오기
# 문서 파서 기본 불러오기 (PyPDFLoader)
# 1. 백터스토어 셋업
# 2. 랭체인 셋업한다 (LCEL)

load_dotenv()
full_path = lambda filename: os.path.join(os.path.dirname(__file__), filename)
DB_DIR = full_path("chroma_db")
COLLECTION_NAME = "my_rag"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

store = Chroma(collection_name=COLLECTION_NAME,
               embedding_function=embeddings,
               persist_directory=DB_DIR)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 문서 기반 QA시스템입니다. 아래 문서만 참고해서 답변하시오. 문서에 관련 내용이 전혀 없으면 답변하지 마시오.\n문서:\n{context}"),
    ("user", "{question}")
])

def format_docs(docs):
    return "\n\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(docs, start=1))

def extract_sources(docs):
    [print(d.metadata) for d in docs]
    return {d.metadata.get("source", "N/A") for d in docs}

def retriever_and_split(inputs):
    retriever = store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(inputs["question"])
    
    print("==========")
    print(docs)
    print("++++++++++")
    print(extract_sources(docs))
    return {"question": inputs["question"],
            "context": format_docs(docs),
            "sources": extract_sources(docs)}

def append_source(d):
    src_lines = "\n".join(f" - {s}" for s in d["sources"])
    return f"{d['answer']}\n\n참고문서:\n{src_lines}"

chain = (
    RunnableLambda(retriever_and_split)    
    | RunnablePassthrough.assign(answer=(prompt | llm | StrOutputParser()))
    | RunnableLambda(append_source)
)

app = Flask(__name__, static_folder="templates")

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/upload")
def upload():
    data = request.files["file"]
    reader = PdfReader(io.BytesIO(data.read()))
    print("store._collection.count()")
    print(store._collection.count())
    chunks = splitter.split_text("\n".join([p.extract_text() for p in reader.pages]))
    chunks = [Document(page_content=p, metadata={"source": data.filename}) for p in chunks]
    store.add_documents(chunks)
    print(store._collection.count())
    return jsonify({"message": "업로드 완료"})

@app.post("/delete")
def delete():
    data = request.files["file"]
    print(store._collection.count())
    store._collection.delete(where={"source": data.filename})
    print(store._collection.count())

    return jsonify({"message": "제거 완료"})

@app.post("/ask")
def ask():
    data = request.get_json().get("message")
    print("=============")
    print(data)
    message = chain.invoke({"question": data})
    return jsonify({"message": message})



if __name__ == "__main__":
    app.run(debug=True)