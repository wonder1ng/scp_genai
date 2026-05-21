import requests, os
from dotenv import load_dotenv

load_dotenv()
NAVER_API_ID = os.getenv("NAVER_API_ID")
NAVER_API_SECRET = os.getenv("NAVER_API_SECRET")

text = "생성형 AI"
# url = "https://openapi.naver.com/v1/search/blog.json"
url = "https://openapi.naver.com/v1/search/news.json"

headers = {
    "X-Naver-Client-Id": NAVER_API_ID,
    "X-Naver-Client-Secret": NAVER_API_SECRET
}

params = {
    "query": text
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

print(data)