import requests, os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

search_url = "https://www.googleapis.com/youtube/v3/search"
video_api_url = 'https://www.googleapis.com/youtube/v3/videos'

search_query = "파이썬 튜토리얼"

search_params = {
    "part": "snippet",
    "q": search_query,
    "type": "video",
    "maxResults": 50,
    "key": API_KEY
}

response = requests.get(search_url, search_params)
data = response.json()
search_results = data["items"]

table = []

table_header = ["index", "title", "view count", "video url"]

for index, result in enumerate(search_results, start=1):

    title = result["snippet"]["title"]
    video_id = result["id"]["videoId"]
    youtube_watch_url = f"https://www.youtube.com/watch?v={video_id}"

    video_params = {
        "part": "statistics",
        "id": video_id,
        "key": API_KEY
    }

    video_response = requests.get(
        video_api_url,
        params=video_params
    )

    print(video_response)

    video_data = video_response.json()

    if "items" in video_data and video_data["items"]:
        view_count = video_data["items"][0]["statistics"]["viewCount"]
    else:
        view_count = "N/A"
    
    table.append([index, title, view_count, youtube_watch_url])
    
print(table_header)

for row in table:
    print(row)