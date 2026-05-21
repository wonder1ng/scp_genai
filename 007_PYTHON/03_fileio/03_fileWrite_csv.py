import csv
base_path = "\\".join(__file__.split("\\")[:-1])
fileName = base_path + "\\file.txt"

data = [
    ["Name", "Age", "City"],
    ["John", 25, "Seoul"],
    ["James", 23, "Busan"],
    ["BobJohn", 24, "Seoul"],
]
with open(fileName, "w", newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(data)
with open(fileName, "r") as f:
    print(f.read())

data2 = [dict(zip(data[0], row)) for row in data[1:]]
print(data2)
with open(fileName, "w", newline="") as f:
    csv_writer = csv.DictWriter(f, data2[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(data2)
with open(fileName, "r") as f:
    print(f.read())