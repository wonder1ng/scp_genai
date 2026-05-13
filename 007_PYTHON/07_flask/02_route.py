from flask import Flask

app = Flask(__name__)

@app.route("/user")
@app.route("/user/<username>")
def show_user_profile(username="익명"):
    return f"<h1>사용자: {username}</h1>"

@app.route("/admin")
def show_admin_profile():
    return "관리자: 홍길동"

@app.route("/product")
@app.route("/product/<int:id>")
def show_product(id=0):
    return f"상품코드: {id}, 상품명: 사과"

if __name__ == "__main__":
    # debug=True: 변경 사항이 실행 중에도 반영됨
    app.run(debug=True)