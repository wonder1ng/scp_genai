import os
from langchain_community.document_loaders import TextLoader

loader = TextLoader(os.path.join(os.path.dirname(__file__), "hbm.txt"), encoding="utf_8")

documents = loader.load()

print(f"불러온 문서의 개수: {len(documents)}")

doc = documents[0]

print(f"page_contesnt (앞의 100글자):\n{doc.page_content[:100]}...\n")
