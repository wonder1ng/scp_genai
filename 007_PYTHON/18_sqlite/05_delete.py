import sqlite3

basePath = "\\".join(__file__.split("\\")[:-1])
conn = sqlite3.connect(basePath + "\\example.db")

cur = conn.cursor()
cur.execute("DELETE FROM users WHERE name=?", ("Bob",))
conn.commit()
cur.execute("select * from users where name='Bob'")
rows = cur.fetchall()
print(rows)

conn.close()