from dotenv import load_dotenv
import requests, os, csv
from google import genai

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

videos = []

with open("video_stats.csv", "r", encoding="utf_8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        videos.append({
            "title": row["title"],
            "views": row["views"],
            "likes": row["likes"],
            "comments": row["comments"],
        })

prompt = f"""
다음 유튜브 영상 데이터를 분석해서: 

1. 어떤 영상이 가장 인기가 있는지
2. 인기 있는 이유는 무엇인지
3. 어떤 주제가 반응이 좋은지
4. 내가 유튜브 채널을 운영하려고 하면 어떤 전략이 좋은지

를 자세히 분석해줘.

답변은 HTML로 포맷팅 해줘

영상 데이터:
{videos}
"""

print(prompt)