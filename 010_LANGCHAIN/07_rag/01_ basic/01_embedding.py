# Retrieval Augmented Generation
# 검색 증강 생성
import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")   # OpenAI의 가장 대중적인 임베딩 모델

text = "고양이가 소파 위에서 잔다."
vec = embeddings.embed_query(text)

sentences = [
    "고양이가 소파 위에서 잔다.",
    "강아지가 침대 위에서 잔다.",
    "파이썬은 인기 있는 프로그래밍 언어다.",
]

vectors = embeddings.embed_documents(sentences)

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

print("=== 우리의 문잔 간 유사도 ===")

for i, s1 in enumerate(sentences):
    for j, s2 in enumerate(sentences):
        if i < j:
            sim = cosine_similarity(vectors[i], vectors[j])
            print(f" {sim:.4f} {s1[:20]} {s2[:20]}")