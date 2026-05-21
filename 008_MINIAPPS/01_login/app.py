from flask import Flask, flash, redirect, render_template, request, session, url_for
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = "hello1234"
app.permanent_session_lifetime = timedelta(minutes=5)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

DATABASE = "user.sqlite3" 

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 결과를 모두 dictionary로 관리
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("create table if not exists users (id integer primary key autoincrement, username text not null, password text not null)")
        cur.execute("select count(*) as count from users")
        count = cur.fetchone()["count"]
        if count == 0:
            cur.execute("insert into users (username, password) values (?, ?)", ("user1", "password1"))
            cur.execute("insert into users (username, password) values (?, ?)", ["user2", "password2"])
        
        cur.execute("select * from users")
        rows = cur.fetchall()

        print("-" * 30)
        for row in rows:
            print(row["id"], row["username"], row["password"])
        print("-" * 30)

        conn.commit()
        conn.close()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("select * from users where username=? and password=?", (username, password))
        user_data = cur.fetchone()
        conn.close()

        if user_data:
            session["user"] = username
            flash("로그인에 성공하였습니다.")
            return redirect(url_for("home"))
        else:
            flash("로그인에 실패하였습니다.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    flash("성공적으로 로그아웃하였습니다.")
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__=="__main__":
    init_db()
    app.run(debug=True)