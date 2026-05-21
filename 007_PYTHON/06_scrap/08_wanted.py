import random, os, csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from tqdm import tqdm
from datetime import datetime

with sync_playwright() as p:
    baseUrl = "https://www.wanted.co.kr"
    browser = p.chromium.launch(headless=False)
    # browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(baseUrl + "/wdlist/518?country=kr&job_sort=job.latest_order&years=-1&locations=all&selected=873&selected=1634&selected=899&selected=655&selected=1024")
    current_height = 0
    new_height = page.evaluate("document.body.scrollHeight")
    while (current_height < new_height):
        current_height = new_height
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(random.uniform(1253, 1834))
        new_height = page.evaluate("document.body.scrollHeight")
        # break
    companies = [e.inner_text() for e in page.locator(".CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu.wds-nkj4w6").all()]
    titles = [e.inner_text() for e in page.locator(".JobCard_JobCard__body__position__NLhOu.wds-vb1aj9").all()]
    etc_infos = [e.inner_text() for e in page.locator(".CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l.wds-nkj4w6").all()]
    urls = [baseUrl + e.get_attribute("href") for e in page.locator(".JobCard_JobCard__aVx71 > a").all()]
    details = []
    for url in tqdm(urls):
        try:
            page.goto(url)
            
            button = page.locator(".wds-16u72rb .wds-bi8qpk")
            if button.count():
                button.wait_for()
                button.hover()
                button.click()

            soup = BeautifulSoup(page.locator(".JobDescription_JobDescription__s2Keo").inner_html(), "html.parser")

            # 줄바꿈 태그 처리
            for br in soup.find_all("br"):
                br.replace_with("\n")
            # 텍스트 추출
            text = soup.get_text("\n", strip=True)
            # 공백 정리
            lines = [line.strip() for line in text.splitlines()]
            lines = [line for line in lines if line]
            details.append("\n".join(lines))
            page.wait_for_timeout(random.uniform(325, 1471))

        except Exception as e:
            print("="*50)
            print(type(e).__name__, e)
            print("="*50)
            details.append("None")

    data = [("company", "title", "etc_info", "detail", "url")]
    data.extend(list(zip(companies, titles, etc_infos, details, urls)))

timeStr = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
base_path = "\\".join(__file__.split("\\")[:-1])
fileName = base_path + f"\\wanted_post_{timeStr}.tsv"
mode = "a+" if os.path.exists(fileName) else "w+"
with open(fileName, mode, newline="", encoding="utf_8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(data) if mode == "w+" else writer.writerows(data[1:])
with open(fileName, "r", encoding="utf_8") as f:
    csv_reader = csv.reader(f, delimiter="\t")
    for row in csv_reader:
        data.append(row)

data = [data[0]] + [e for e in data if any(v in e[2] for v in ["신입", "인턴", "무관"])]
fileName = base_path + f"\\wanted_post_junior_{timeStr}.tsv"
mode = "a+" if os.path.exists(fileName) else "w+"
with open(fileName, mode, newline="", encoding="utf_8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(data) if mode == "w+" else writer.writerows(data[1:])
with open(fileName, "r", encoding="utf_8") as f:
    csv_reader = csv.reader(f, delimiter="\t")
    for row in csv_reader:
        data.append(row)