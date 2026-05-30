import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

loader = TextLoader(os.path.join(os.path.dirname(__file__), "hbm.txt"), encoding="utf_8")
documents = loader.load()

contents = documents[0].page_content
print(f"원본 글자수: {len(contents)}")

# 일반적으로 1000:200 / 1500:300 / 2000:500 정도로 실제 chunking 내용 보고 판단함
char_splitter = CharacterTextSplitter(
    separator="\n\n",   # 이것을 목표로 하는데 안 될 수 있음
    chunk_size=500,     # 위에 조각이 작으면 500개 될 때까지 합침
    chunk_overlap=100   # 문장이 중간에 짤리지 않도록 겹치게 짜름
)

chunks_char = char_splitter.split_documents(documents)
print(f"CharSplitter {len(chunks_char)}")
print(f"첫 청크 글자 수: {len(chunks_char[0].page_content)}")
[print(len(p.page_content)) for p in chunks_char]

recur_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks_recur = recur_splitter.split_documents(documents)
print(f"[RecurSplitter] {len(chunks_recur)}")
print(f"첫 청크 글자 수: {len(chunks_recur[0].page_content)}")
[print(len(p.page_content)) for p in chunks_recur]