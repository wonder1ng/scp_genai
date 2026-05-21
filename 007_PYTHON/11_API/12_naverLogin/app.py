from flask import Flask, redirect, render_template, request, session, url_for
import  os
from dotenv import load_dotenv
import requests

load_dotenv()
NAVER_API_ID = os.getenv("NAVER_API_ID")
NAVER_API_SECRET = os.getenv("NAVER_API_SECRET")
CALLBACK_URI = os.getenv("NAVER_REDIRECT_URI")
app = Flask(__name__)
app.secret_key = os.getenv("id")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/naver/callback")
def naver_callback():
    code = request.args.get("code")
    state = request.args.get("state")   # state: 제출값과 반환값 검증용 사용자 시크릿
    print("state")
    print(state)
    token_url = (
        f"https://nid.naver.com/oauth2.0/token?"
        f"grant_type=authorization_code&client_id={NAVER_API_ID}"
        f"&client_secret={NAVER_API_SECRET}&code={code}&state={state}"
    )

    token_reponse = requests.get(token_url).json()
    access_token = token_reponse.get("access_token")
    print(access_token)

    profile_url = (
        f"https://openapi.naver.com/v1/nid/me"
    )

    headers = {"Authorization": f"Bearer {access_token}"}

    profile = requests.get(profile_url, headers=headers).json()
    print("서버측 사용자 정보 응답:", profile)

    session["user"] = profile["response"]
    
    return redirect(url_for("index"))

@app.route("/login")
def naver_login():
    auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&client_id={NAVER_API_ID}"
        f"&redirect_uri={CALLBACK_URI}&state=HELLO"
    )

    auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&client_id={NAVER_API_ID}"
        f"&redirect_uri={CALLBACK_URI}&state=HELLO"
    )
    print(auth_url)
    return redirect(auth_url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)