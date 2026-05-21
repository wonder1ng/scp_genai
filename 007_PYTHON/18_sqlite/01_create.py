import sqlite3

basePath = "\\".join(__file__.split("\\")[:-1])
conn = sqlite3.connect(basePath + "\\example.db")

cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGET PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL)")

conn.commit()
conn.close()