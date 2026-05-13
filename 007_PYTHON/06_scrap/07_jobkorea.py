import requests, random, time, os
from tqdm import tqdm
from bs4 import BeautifulSoup

baseUrl = "https://www.jobkorea.co.kr"
subUrl = "/recruit/joblist?&local=I000,B020,B030,B031,B150,B160,B170&duty=1000236,1000237,1000242,1000418,1000422,1000423&career=1,8&order=2#anchorGICnt_"
# subUrl = "/recruit/joblist?&local=I000,B020,B030,B031,B150,B160,B170&duty=1000236,1000237,1000242,1000418,1000422,1000423&order=2#anchorGICnt_"

url = baseUrl + "/Recruit/Home/_GI_List/"

payload = {
    "Page": 1,
    "PageSize": 50,
    "SearchType": 1,

    "local": "I000,B020,B030,B031,B150,B160,B170",
    "duty": "1000236,1000237,1000242,1000418,1000422,1000423",
    "career": "1,8",

    "order": "2"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.jobkorea.co.kr/",
    "X-Requested-With": "XMLHttpRequest"
}

res = requests.post(
    url,
    data=payload,
    headers=headers
)

data = [["company", "title", "etc_info", "url"]]
for num in range(1, 999999):
    payload["Page"] = num
    res = requests.post(url, data=payload, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        if soup.select("#imgCaptcha"):
            print("캡챠 제거 요망")
        else:
            for post in tqdm(soup.select(".devloopArea")):

                postUrl = baseUrl + post.select_one("strong a.link.normalLog")["href"].split("?")[0]
                result = requests.get(postUrl, headers=headers)
                soupPost = BeautifulSoup(result.text, "html.parser")
                details = soupPost.select_one("div.ml-auto > div > div > div.flex.flex-col")
                try:
                    detail = "   ".join([_.text for _ in details.select("div > div >div > div > span ")] + [_.text for _ in details.select("div > div >div > div li")])
                except:
                    detail = "None"
                data.append([
                post.select_one(".link.normalLog").text,
                post.select_one("strong a.link.normalLog")["title"],
                postUrl,
                ", ".join([" ".join(cell.text.split()) for cell in post.select("p.etc > span") if cell.text]),
                detail
                ])
            if soup.select(".nodata"):
                break
            # time.sleep(random.uniform(1, 13))

basePath = "\\".join(__file__.split("\\")[:-1])
fileName = basePath + "\\jobkorea_post.tsv"
mode = "a+" if os.path.exists(fileName) else "w+"
with open(fileName, mode, newline="", encoding="utf_8") as f:
    [f.writelines("\t".join(post) + "\n") for post in data] if mode == "w+" else [f.writelines("\t".join(post) + "\n") for post in data[1:]]