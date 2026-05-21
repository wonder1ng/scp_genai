import requests, csv, os
base_path = "\\".join(__file__.split("\\")[:-1])
with open(base_path + "\\env.txt", "r", encoding="utf_8") as f:
    res = [line.split("=")[1] for line in f.read().split("\n")]
    baseUrl = res[0]
    id = res[1]
    pw = res[2]

data = []
for i in (1, 2):
    res = requests.get(f"{baseUrl}/api/products?page={i}")
    data += res.json()["items"]
for p in data:
    res = requests.get(f"{baseUrl}/api/product/{p["product_id"]}")
    detail = res.json()
    p["sales_count"] = detail.get("sales_count")
    p["reviews"] = detail.get("reviews")

base_path = "\\".join(__file__.split("\\")[:-1])
fileName = base_path + "\\logout.tsv"
with open(fileName, "w", newline="", encoding="utf_8") as f:
    csv_writer = csv.DictWriter(f, data[0].keys(), delimiter="\t")
    csv_writer.writeheader()
    csv_writer.writerows(data)
with open(fileName, "r", encoding="utf_8") as f:
    csv_reader = csv.DictReader(f)
    [print(r) for r in csv_reader]

from playwright.sync_api import sync_playwright

data = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(baseUrl)
    page.locator("#uid").fill(id)
    page.locator("#upw").fill(pw)
    page.locator("#loginBtn").click()
    for i in range(1, 6):
        res = page.request.get(f"{baseUrl}/api/products?page={i}")
        data += res.json()["items"]
    for p in data:
        res = page.request.get(f"{baseUrl}/api/product/{p["product_id"]}")
        detail = res.json()
        p["sales_count"] = detail.get("sales_count")
        p["reviews"] = detail.get("reviews")

base_path = "\\".join(__file__.split("\\")[:-1])
fileName = base_path + "\\login.tsv"
with open(fileName, "w", newline="", encoding="utf_8") as f:
    csv_writer = csv.DictWriter(f, data[0].keys(), delimiter="\t")
    csv_writer.writeheader()
    csv_writer.writerows(data)
with open(fileName, "r", encoding="utf_8") as f:
    csv_reader = csv.DictReader(f)
    [print(r) for r in csv_reader]