import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_chroma import Chroma
from pypdf import PdfReader

# 랭체인 기본 불러오기
# 문서 파서 기본 불러오기 (PyPDFLoader)
# 1. 백터스토어 셋업
# 2. 랭체인 셋업한다 (LCEL)

load_dotenv()
full_path = lambda filename: os.path.join(os.path.dirname(__file__), filename)
DB_DIR = full_path("chroma_db")
DATA_DIR = full_path("data")
COLLECTION_NAME = "my_rag_db"
os.makedirs(DATA_DIR, exist_ok=True)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma(collection_name=COLLECTION_NAME,
               embedding_function=embeddings,
               persist_directory=DB_DIR)
retriever = store.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 문서 기반 QA시스템입니다. 아래 문서만 참고해서 답변하시오. 문서에 관련 내용이 전혀 없으면 답변하지 마시오.\n문서:\n{context}"),
    MessagesPlaceholder("history"),
    ("user", "{question}")
])

def format_docs(docs):
    return "\n--\n".join(d.page_content for d in docs)

def debug_prompt(prompt):
    print("\n=== PROMPT ===")
    for msg in prompt.messages:
        print(f"[{msg.type.upper()}]\n{msg.content}")
    print("\n=== 출력 끝 ===\n")
    return prompt

chain = (
    RunnablePassthrough.assign(context=lambda x: format_docs(retriever.invoke(x["question"])))
    | prompt
    | RunnableLambda(debug_prompt)
    | llm
    | StrOutputParser()
)

history = InMemoryChatMessageHistory()

app = Flask(__name__, static_folder="templates")

@app.get("/")
def index():
    """"""
    return render_template("index.html")

def delete_document(source):
    store._collection.delete(where={"source": source})

    path = os.path.join(DATA_DIR, source)
    if os.path.exists(path):
        os.remove(path)
    
    return True

@app.delete("/files/<path:source>")
def remote_file(source):
    existed = delete_document(source)
    msg = f"'{source}' 삭제 완료" if existed else f"'{source}'는 목록에 없었습니다."
    return jsonify({"message": msg, "files": list_documents()}), 204

def list_documents():
    return [{"source": s, "chunks": c} for s, c in sorted(_distinct_sources().items())]

def _distinct_sources():
    data = store._collection.get(include=["metadatas"])
    
    counts: dict[str, int] = {}
    for m in data.get("metadatas", []):
        src = (m or {}).get("source", "N/A")
        counts[src] = counts.get(src, 0) + 1
    return counts

@app.get("/files")
def files():
    return jsonify({"files": list_documents()})

def add_my_pdf_file(path):
    docs = PyPDFLoader(path).load()
    for d in docs:
        d.metadata["source"] = os.path.basename(path)
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    store.add_documents(chunks)

@app.post("/upload")
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "파일이 없습니다."}), 400
    
    path = os.path.join(DATA_DIR, file.filename)
    print(path)
    file.save(path)
    add_my_pdf_file(path)

    return jsonify({"message": "업로드 완료"})

def call_langchain_qa(question):
    if store._collection.count() == 0:
        return "먼저 PDF 문서를 업로드해 주세요"
    
    print(f"질문: {question}")
    answer = chain.invoke({
        "question": question,
        "history": history.messages[-10:],
    })
    history.add_user_message(question)
    history.add_ai_message(answer)

    return answer

@app.post("/ask")
def ask():
    question = request.get_json().get("question")
    print("=============")
    print("question:", question)
    answer = call_langchain_qa(question)
    print("=============")
    print("answer:", answer)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)