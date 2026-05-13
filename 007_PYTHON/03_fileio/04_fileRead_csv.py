import csv
basePath = "\\".join(__file__.split("\\")[:-1])
fileName = basePath + "\\file.txt"

with open(fileName, "r") as f:
    csv_reader = csv.reader(f)
    [print(r) for r in csv_reader]

with open(fileName, "r") as f:
    csv_reader = csv.DictReader(f)
    [print(r) for r in csv_reader]