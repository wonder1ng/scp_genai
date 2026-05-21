import sqlite3

base_path = "\\".join(__file__.split("\\")[:-1])
conn = sqlite3.connect(base_path + "\\example.db")

cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGET PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL)")

conn.commit()
conn.close()