from flask import Flask, render_template, request, session, url_for, redirect, flash
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
        cur.execute("create table if not exists users (id integer primary key autoincrement, username text not null, password text not null, email text)")
        cur.execute("select count(*) as count from users")
        count = cur.fetchone()["count"]
        if count == 0:
            cur.execute("insert into users (username, password, email) values (?, ?, ?)", ("user1", "password1", "user1@example.com"))
            cur.execute("insert into users (username, password) values (?, ?)", ["user2", "password2"])
        
        cur.execute("select * from users")
        rows = cur.fetchall()

        print("-" * 30)
        for row in rows:
            row = dict(row)
            print(row)
            print(row["id"], row["username"], row["password"], row.get("email", None))
        print("-" * 30)

        conn.commit()
        conn.close()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    username = session.get("user", None)
    if username:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("select * from users where username=?", [username])
        user = cur.fetchone()
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            email = request.form.get("email")
            print("username, password, email")
            print(username, password, email)
            if not username: username = user[1]
            if not password: password = user[2]
            if not email: email = user[3]
            
            cur.execute("update users set username=?, password=?, email=? where username=?", (username, password, email, username))
            conn.commit()
            cur.execute("select * from users where username=?", [username])
            user = cur.fetchone()

        conn.close()
        return render_template("profile.html", user=user)
    else:
        flash("로그인을 필요로 합니다.")
        return redirect(url_for("signin"))
    
@app.route("/profile/delete")
def profileDelete():
    username = session.get("user", None)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("delete from users where username=?", [username])
    conn.commit()
    flash("성공적으로 탈퇴하였습니다.")
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("select * from users where username?", [username])
        existing_user = cur.fetchone()

        if existing_user:
            flash("해당 ID는 사용할 수 없습니다.")
            conn.close()
            return redirect(url_for("signin"))
        
        cur.execute("insert into users (username, password, email) values (?,?,?)", (username, password, email))
        conn.commit()
        conn.close()

        flash("회원가입이 성공적으로 완료되었습니다.")
        return redirect(url_for("login"))
    return render_template("signin.html")

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