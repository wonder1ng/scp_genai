import google.oauth2.credentials
import google_auth_oauthlib.flow

base_path = "\\".join(__file__.split("\\")[:-1])
from flask import Flask, redirect, request, session, url_for, render_template
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:5000/callback"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/login")
def login():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        # "access_type": "offline",
        "prompt": "consent"
    }

    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return redirect(auth_url)


@app.route("/callback")
def callback():
    print("request.get_json()")
    print(request)
    code = request.args.get("code")

    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    token_response = requests.post(
        GOOGLE_TOKEN_URL,
        data=token_data
    )

    token_json = token_response.json()

    access_token = token_json.get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    user_info_response = requests.get(
        GOOGLE_USERINFO_URL,
        headers=headers
    )

    user_info = user_info_response.json()

    session["user"] = {
        "name": user_info.get("name"),
        "email": user_info.get("email"),
        "picture": user_info.get("picture")
    }

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)