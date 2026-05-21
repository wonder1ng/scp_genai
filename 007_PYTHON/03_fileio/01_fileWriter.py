base_path = "\\".join(__file__.split("\\")[:-1])
fileName = base_path + "\\file.txt"
with open(fileName, "w") as f:
    f.write("Hello, World")
with open(fileName, "r") as f:
    print(f.read())