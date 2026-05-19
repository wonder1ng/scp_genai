from flask import Flask, session

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/set-session")
def set_session():
    session["username"] = "spc2026"
    return "세션 저장 완료"

@app.route("/get-session")
def get_session():
    if "username" in session:
        return f"세션에서 당신의 정보를 찾았습니다. {session["username"]}"
    return "세션 정보가 없습니다."
    
if __name__ == "__main__":
    app.run(debug=True)