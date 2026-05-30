import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

loader = PyPDFLoader(os.path.join(os.path.dirname(__file__), "javascriptSecureCoding.pdf"))
pages = loader.load()

print(f"PDF 페이지 수: {len(pages)}\n")

# 일반적으로 1000:200 / 1500:300 / 2000:500 정도로 실제 chunking 내용 보고 판단함
char_splitter = CharacterTextSplitter(
    separator="\n\n",   # 이것을 목표로 하는데 안 될 수 있음
    chunk_size=500,     # 위에 조각이 작으면 500개 될 때까지 합침
    chunk_overlap=100   # 문장이 중간에 짤리지 않도록 겹치게 짜름
)

chuncks = char_splitter.split_documents(pages)
print(f"청킹 후 문서 갯수: {len(chuncks)}\n")

first = chuncks[0]
print(first.metadata)
print(first.page_content)
print("=" * 30)