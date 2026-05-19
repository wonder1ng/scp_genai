import requests

url = "https://api.github.com/search/repositories"

keyword = "chatbot"

params = {
    "q": keyword,
    "per_page": 100,
    "page": 2
}

resp = requests.get(url, params)
data = resp.json()

if "items" in data:
    repos = data["items"]
    for repo in repos:
        name = repo["name"]
        html_url = repo["html_url"]
        full_name = repo["full_name"]
        desc = repo["description"]
        print(f"레포 이름: {name}, 풀네임: {full_name}, 레포 URL: {html_url}, 설명: {desc}")
