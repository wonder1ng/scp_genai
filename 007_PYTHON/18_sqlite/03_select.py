import sqlite3

base_path = "\\".join(__file__.split("\\")[:-1])
conn = sqlite3.connect(base_path + "\\example.db")

cur = conn.cursor()
cur.execute("select * from users")
rows = cur.fetchall()
print(rows)

conn.close()