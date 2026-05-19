import requests

url = "https://api.github.com/users/lovehyun/repos"

resp = requests.get(url)
repos = resp.json()
data = []

for repo in repos:
    name = repo["name"]
    html_url = repo["html_url"]
    desc = repo["description"]
    data.append({"name": name, "html_url": html_url, "desc": desc})

print(f"레포 이름: {name}, 레포 URL: {html_url}, 설명: {desc}")
for d in data:
    print(f"{d["name"]:<30} {d["html_url"]:<50} {str(d["desc"]):<50}")