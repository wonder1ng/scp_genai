import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI

load_dotenv()
app = Flask(__name__, static_folder="public")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"

reviews = []

# --------------------
# API 라우팅
# --------------------
@app.route("/api/reviews", methods=["POST"])
def add_review():
    data = request.get_json()
    reviews.append({"comment": data["comment"], "rating": data["rating"]})
    return jsonify({"reviews": reviews})

@app.route("/api/reviews")
def get_review():
    lang = request.args.get("lang")
    response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"당신은 전문 {lang} 번역가입니다. 다음의 내용을 {lang}으로 번역하세요. 사족 넣지말고 번역한 내용만 반환하세요."},
                    {"role": "user", "content": request.args.get("message")}
                ]
            )
    print(response.choices[0].message.content)
    return jsonify({"message": response.choices[0].message.content})

@app.route("/api/ai-summary")
def get_ai_summary():
    avg_rating = sum([int(e.get("rating")) for e in reviews]) / len(reviews)
    response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "쇼핑물의 리뷰를 요약하세요.\n긍정과 부정 반응으로 나눠 요약하세요."},
                    {"role": "user", "content": "\n다음 리뷰\n".join([e.get("comment") for e in reviews])}
                ]
            )
    print("response")
    print(response)
    return jsonify({"message": response.choices[0].message.content, "rating": f"{avg_rating:.2f}"})

# --------------------
# 웹 서비스 라우팅
# --------------------
@app.route("/")
def index():
    return send_from_directory("public", "index.html")

if __name__ == "__main__":
    app.run(debug=True)