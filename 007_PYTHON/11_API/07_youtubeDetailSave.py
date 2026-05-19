import requests, os, csv
from dotenv import load_dotenv

# .env 로드
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

# API URL
video_api_url = 'https://www.googleapis.com/youtube/v3/videos'

video_ids = []

basePath = "\\".join(__file__.split("\\")[:-1])
fileName = basePath + "\\search_result.csv"
with open(fileName, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        video_ids.append(row["video_id"])

params = {
    "part": "snippet,statistics",
    "id": ",".join(video_ids),
    "key": API_KEY
}

response = requests.get(video_api_url, params)
data = response.json()

table = []

table_header = ["index", "title", "view_count", "like_count", "comment_count"]

fileName = basePath + "\\video_stats.csv"
with open(fileName, "w", newline="", encoding="utf_8") as f:
    writer = csv.writer(f)
    writer.writerow(table_header)

    for item in data["items"]:
        video_id = item["id"]
        title = item["snippet"]["title"]
        stats = item["statistics"]
        view_count = stats.get("viewCount", 0)
        like_count = stats.get("likeCount", 0)
        comment_count = stats.get("comment", 0)

        writer.writerow([video_id, title, view_count, like_count, comment_count])