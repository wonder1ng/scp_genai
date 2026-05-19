from flask import Flask, make_response, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션 암호화 키

users = [
    {"name": "Alice", "id": "alice", "pw": "alice"},
    {"name": "Bob", "id": "bob", "pw": "bob1234"},
    {"name": "Charlie", "id": "charlie", "pw": "hello"},
]

@app.route("/dashboard")
def welcome():
    user = session.get("user")
    return render_template("dashboard.html", name=user["name"])

@app.route("/")
def home():
    if session.get("user"):
        return redirect(url_for("welcome"))
    return render_template("index.html")

@app.route("/", methods=["POST"])
def login():
    id = request.form.get("id")
    pw = request.form.get("pw")

    user = next((u for u in users if u["id"] == id and u["pw"] == pw), None)

    if user:
        session["user"] = user
        error = None
        return redirect(url_for("welcome"))
    else:
        error = "Invalid ID or password"
    return render_template("index.html", error = error)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        user = session.get("user")
        if not user:
            return redirect(url_for("home")) # 로그인 안됐으면 로그인 페이지로 강제 이동
        
        return render_template("profile.html", user=user)
    elif request.method == "POST":
        user = session.get("user")
        user["pw"] = request.get_data().decode("utf_8").split("=")[-1]
        session["user"] = user
        [u.update({"pw": user["pw"]}) for u in users if u.get("id") == user["id"]]
        return render_template("profile.html", user=user)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)