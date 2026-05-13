# from urllib.request import urlopen
# from bs4 import BeautifulSoup

# soup = BeautifulSoup(urlopen("https://news.naver.com/section/105"), "html.parser")
# headlines = soup.select("div > div > div > div > div > div > ul > li > div > div > div > a")
# data = [["url", "content"]]
# for headline in headlines:
#     article = BeautifulSoup(urlopen(headline["href"]))
#     data.append([headline["href"], article.select_one("article").get_text().replace("\n", " ")])

# articles = soup.select("div.section_latest > div > div.section_latest_article._CONTENT_LIST._PERSIST_META > div > ul > li > div > div > div.sa_text > a")
# for article in articles:
#     content = BeautifulSoup(urlopen(article["href"]))
#     data.append([article["href"], content.select_one("article").get_text().replace("\n", " ")])

# basePath = "\\".join(__file__.split("\\")[:-1])
# fileName = basePath + "\\naver_news_IT.csv"

# with open(fileName, "w", newline="", encoding="utf_8") as f:
#     [f.writelines("\t".join(one) + "\n") for one in data]
# with open(fileName, "r", encoding="utf_8") as f:
#     print(f.read())

from playwright.sync_api import sync_playwright
import csv
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://news.naver.com/section/105")
    headlines = page.locator("html > body> div > div > div > div > div > div > ul > li > div > div > div > a")
    data = [["url", "content"]]
    for headline in headlines.all():
        url = headline.get_attribute("href")
        page.goto(url)
        page.wait_for_selector("#newsct_article")
        data.append([url, page.locator("#newsct_article").inner_text().strip().replace("\n", " ")])
        page.go_back()

    articles = page.locator("div.section_latest > div > div.section_latest_article._CONTENT_LIST._PERSIST_META > div > ul > li > div > div > div.sa_text > a")
    for article in articles.all():
        url = article.get_attribute("href")
        page.goto(url)
        page.wait_for_selector("#newsct_article")
        data.append([url, page.locator("#newsct_article").inner_text().strip().replace("\n", " ")])
        page.go_back()

    basePath = "\\".join(__file__.split("\\")[:-1])
    fileName = basePath + "\\naver_news_IT2.tsv"

    with open(fileName, "w", newline="", encoding="utf_8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(data)
    with open(fileName, "r", encoding="utf_8") as f:
        csv_reader = csv.reader(f, delimiter="\t")
        for row in csv_reader:
            data.append(row)
    print(data)