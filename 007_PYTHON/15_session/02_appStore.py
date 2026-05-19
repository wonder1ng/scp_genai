from flask import Flask, make_response, request, session
from flask_session import Session

basePath = "\\".join(__file__.split("\\")[:-1])

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션 암호화 키
app.config["SESSION_TYPE"] = "filesystem"   # 세션 db or file
app.config["SESSION_FILE_DIR"] = basePath + "\\.sessions"   # 세션 저장할 폴더명
app.config["SESSION_PERMANENT"] = False # 브라우저 닫히면 삭제
app.config["SESSION_USE_SIGNER"] = True # 세션 쿠키 서명에 사용

@app.route("/set-session")
def set_session():
    session["username"] = "spc2026"
    session["fullname"] = "홍길동"
    session["dob"] = "2020/05/05"
    session["hobby"] = "유튜브, 쇼핑, 게임"

    return "세션 저장 완료"

@app.route("/get-session")
def get_session():
    if "username" in session:
        # return f"세션에서 당신의 정보를 찾았습니다. {session["username"]}"
        return f"세션에서 당신의 정보를 찾았습니다. {session.values()}"
    return "세션 정보가 없습니다."
    
if __name__ == "__main__":
    app.run(debug=True)