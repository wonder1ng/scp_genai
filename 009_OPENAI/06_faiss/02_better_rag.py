from dotenv import load_dotenv
from openai import OpenAI
import os, numpy as np, faiss

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

documents = [
    "한국소프트웨어저작권협회는 SPC라는 약자를 갖고 있고, 다양한 국내 기업의 SW 라이센스와 저작권을 다루는 곳입니다.",
    "홍길동은 2020년 1월 1일 생으로, 강원도 설빙산에서 태어났고, 그곳에서 호랑이를 잡아먹으며 성장하였습니다.",
    "Python은 개발 언어 중에 가장 쉽다고 하는데, 그렇게 쉬운 언어는 아닙니다."
]

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return np.array(response.data[0].embedding)

doc_embeddings = np.array([get_embedding(doc) for doc in documents])
index = faiss.IndexFlatL2(1536) # text-embedding-ada-002의 임베딩 차원
index.add(doc_embeddings)

def rag_query(user_query):
    query_embedding = get_embedding(user_query)
    print(query_embedding)
    distance, indices = index.search(np.array([query_embedding]), k=1)
    retrieved_doc = documents[indices[0][0]]
    
    true_distance = np.sqrt(distance[0][0])
    similarity_score = 1 / (1 + true_distance)

    print("="*30)
    print(f"사용자 질문: {user_query}")
    print(f"검색된 문서: {retrieved_doc}")
    print(f"유사도 점수: {similarity_score:.3f}")

    if similarity_score < 0.65:
        return "해당 내용은 적합한 답변을 찾을 수 없습니다."

    prompt = f"""
        아래 질문을 보고 답변하시오.
        [사용자 질문]
        {user_query}
        [관련 자료]
        {retrieved_doc}
    """

    print("="*30)
    print(f"질문과 가까운 벡터 인덱스: {indices}, 그 거리: {distance}")
    print("="*30)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 친절한 AI도우미 입니다."},
            {"role": "user", "content": prompt},
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

# rag_query("한국소프트웨어저작권협회")
rag_query("홍길동은 누구인가요?")