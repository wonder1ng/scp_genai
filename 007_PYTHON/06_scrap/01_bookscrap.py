import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

soup = BeautifulSoup(urlopen("https://books.toscrape.com/"), "html.parser")
book_li = soup.select("#default > div > div > div > div > section > div:nth-child(2) > ol > li")

data = [["title", "stars", "price"]]
for book in book_li:
    data.append([
    book.select_one("article > h3 > a")["title"],
    book.select_one("article > p")["class"][1],
    book.select_one("article > div.product_price > p.price_color").text])

base_path = "\\".join(__file__.split("\\")[:-1])
fileName = base_path + "\\books_toscrape.csv"

with open(fileName, "w", newline="", encoding="utf_8") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(data)
with open(fileName, "r", encoding="utf_8") as f:
    print(f.read())
