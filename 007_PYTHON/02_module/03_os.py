import os

print(os.getcwd())
# print(os.mkdir("Hello"))
# print(os.rmdir("Hello"))

os.chdir("./..")
cwd = os.getcwd()

print(cwd)
print(os.listdir(cwd))
