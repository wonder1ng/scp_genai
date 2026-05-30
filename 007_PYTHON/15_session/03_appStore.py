from flask import Flask, make_response, request, session
from flask_session import Session

base_path = "\\".join(__file__.split("\\")[:-1])

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션 암호화 키
app.config["SESSION_TYPE"] = "filesystem"   # 세션 db or file
app.config["SESSION_FILE_DIR"] = base_path + "\\.sessions"   # 세션 저장할 폴더명
app.config["SESSION_PERMANENT"] = False # 브라우저 닫히면 삭제
app.config["SESSION_USE_SIGNER"] = True # 세션 쿠키 서명에 사용

Session(app)

@app.route("/")
def main():
    if "username" in session:
        # return f"세션에서 당신의 정보를 찾았습니다. {session["username"]}"
        return f"세션에서 당신의 정보를 찾았습니다. {list(session.values())}"
    session["username"] = "spc2026"
    session["fullname"] = "홍길동"
    session["dob"] = "2020/05/05"
    session["hobby"] = "유튜브, 쇼핑, 게임"

    return "첫 방문이시군요. 또 오세요."

if __name__ == "__main__":
    app.run(debug=True)