import os
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(os.path.join(os.path.dirname(__file__), "javascriptSecureCoding.pdf"))
pages = loader.load()

print(f"PDF 페이지 수: {len(pages)}")

for p in pages:
    if p.page_content.strip():
        print(f"발견한 내용이 있는 첫페이지의 metadata:\n{p.metadata}")
        print(f"페이지 내용 (앞 100글자):\n{p.page_content[:100]}")
        break