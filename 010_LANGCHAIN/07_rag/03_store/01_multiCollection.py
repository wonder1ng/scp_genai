import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()
def path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)
DB_DIR = path("chroma_db")


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def build_document(file_path, collection):
    store = Chroma(collection_name=collection,
                   embedding_function=embeddings,
                   persist_directory=DB_DIR)
    if store._collection.count() > 0:
        return store
    
    docs = TextLoader(file_path, encoding="utf_8").load()
    chuncks = splitter.split_documents(docs)
    for c in chuncks:
        c.metadata["source"] = os.path.basename(file_path)
    
    return Chroma.from_documents(chuncks, 
                                 embeddings, 
                                 collection_name=collection, 
                                 persist_directory=DB_DIR)

collections = {"nvme": build_document(path("nvme.txt"), "nvme"),
               "hbm": build_document(path("hbm.txt"), "hbm")}
for name, stroe in collections.items():
    print(f"컬렉션: {name}, 청크 개수: {stroe._collection.count()}")

def search_in(name, query, k=2):
    return collections[name].similarity_search(query, k=k)

def search_all(query, k_per=2):
    results = []
    for name, store in collections.items():
        for doc in store.similarity_search(query, k=k_per):
            doc.metadata["collection"] = name
            results.append(doc)
    return results

query = "PCIe 인터페이스 속도는?"

print("\n=== 'nvme' 컬렉션 ===")
for d in search_in("nvme", query):
    print(f" -> {d.page_content}...")

print("\n=== 'hbm' 컬렉션 ===")
for d in search_in("hbm", query):
    print(f" -> {d.page_content}...")

print("\n=== 'nvme, hbm' 컬렉션 ===")
for d in search_all(query):
    print(f" -> [{d.metadata['collection']}] {d.page_content}...")