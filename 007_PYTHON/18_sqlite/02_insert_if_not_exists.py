import sqlite3

basePath = "\\".join(__file__.split("\\")[:-1])
conn = sqlite3.connect(basePath + "\\example.db")

cur = conn.cursor()
cur.execute("select count(*) from users")
rows = cur.fetchall()[0]    # [(2,)]
print(rows)
cur.execute("select count(*) from users")
rows = cur.fetchone()[0]    # (2,)
print(rows)

# cur.execute("UPDATE users SET age=? WHERE name=?", (33, "Bob"))
# cur.execute("select * from users where name=?", ('Bob', ))
# rows = cur.fetchall()
print(rows)

conn.close()