import sqlite3

basePath = "\\".join(__file__.split("\\")[:-1])
conn = sqlite3.connect(basePath + "\\example.db")

cur = conn.cursor()
cur.execute("select * from users")
rows = cur.fetchall()
print(rows)

conn.close()