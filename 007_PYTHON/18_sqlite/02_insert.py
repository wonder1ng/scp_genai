import sqlite3

base_path = "\\".join(__file__.split("\\")[:-1])
conn = sqlite3.connect(base_path + "\\example.db")

cur = conn.cursor()
cur.execute("INSERT INTO users(name, age) VALUES ('ALICE', 30)")
cur.execute("INSERT INTO users(name, age) VALUES ('Bob', 25)")
conn.commit()
cur.execute("SELECT COUNT(*) FROM users")
cnt = cur.fetchone[0]
print(cnt)

if cnt == 0:
    cur.execute("INSERT INTO users(name, age) VALUES (?, ?)", ('ALICE', 30))
    cur.execute("INSERT INTO users(name, age) VALUES (?, ?)", ('Bob', 25))
    conn.commit()
else:
    print("이미 테이블에 데이터가 있습니다.")

conn.close()