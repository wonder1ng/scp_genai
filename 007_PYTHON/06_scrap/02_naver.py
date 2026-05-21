import csv, requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

print(f"{' naver aticles ':=^40}")
articles = requests.get("https://www.naver.com/nvhaproxy/v2/pc/lazy?blockCodeList=PC-MEDIA-WRAPPER&target=PC-MEDIA-NEWS")
articles.encoding = "utf_8"
# data = []
# for v in articles.json()["PC-MEDIA-WRAPPER"]["blocks"][0]["blocks"]:
#     print("="*30)
#     if v.get("@type") and v.get("materials"):
#         # print(v)
#         # print(v["materials"])
#         # print(len(v["materials"]))
#         for v2 in v["materials"]:
#             # print(v2["title"])
#             # print(v2["url"])
#             # print(v2["officeName"])
#             data.append(v2)
#     else: 
#         print(v.get("PC-NEWS-CHANNEL-BLOCK"))
data= articles.json()["PC-MEDIA-WRAPPER"]["blocks"][0]["blocks"][0]["materials"]

base_path = "\\".join(__file__.split("\\")[:-1])
fileName = base_path + "\\naver_articles.csv"

with open(fileName, "w", newline="", encoding="utf_8") as f:
    csv_writer = csv.DictWriter(f, data[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(data)
with open(fileName, "r", encoding="utf_8") as f:
    print(f.read())



print(f"{' naver aticles2 ':=^40}")
import json

soup = BeautifulSoup(urlopen("https://www.naver.com/"), "html.parser")
script = soup.find_all("script")[5]
data = json.loads(script.text.split("\n")[5].split(" = ")[1])["materials"]

base_path = "\\".join(__file__.split("\\")[:-1])
fileName = base_path + "\\naver_articles2.csv"

with open(fileName, "w", newline="", encoding="utf_8") as f:
    csv_writer = csv.DictWriter(f, data[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(data)
with open(fileName, "r", encoding="utf_8") as f:
    print(f.read())
