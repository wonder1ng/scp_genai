import requests, os, csv
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

url = "https://www.googleapis.com/youtube/v3/search"

search_query = "파이썬 튜토리얼"

params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 50,
    'key': API_KEY
}

response = requests.get(url, params)
data = response.json()
print(data)

basePath = "\\".join(__file__.split("\\")[:-1])
fileName = basePath + "\\search_result.csv"
with open(fileName, "w", newline="", encoding="utf_8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "video_id", "video_url", "description"])

    for item in data["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        description = item["snippet"]["description"]

        print(f"제목: {title}, URL: {video_url}, 설명: {description}")
        print("-"*40)

        writer.writerow([title, video_id, video_url, description])