import sqlite3

basePath = "\\".join(__file__.split("\\")[:-1])

class MyDatabase():
    def __init__(self):
        self.db = sqlite3.connect(basePath+"\\board.sqlite", check_same_thread=False)
        self.cursor = self.db.cursor()
        self.cursor.execute("create table if not exists board (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT NOT NULL)")

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
    
    def excute_fetch(self, query, args={}):
        print(query, args)
        self.cursor.execute(query, args)
        result = self.cursor.fetchall()
        return result
    
    def commit(self):
        self.db.commit()

    def close(self):
        self.close()