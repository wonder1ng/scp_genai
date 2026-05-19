from flask import Flask, render_template
# 사용자 함수
from user_routes import user_blueprint
from admin_routes import admin_blueprint
from product_routes import product_blueprint

app = Flask(__name__)
# Blueprint: 기능별로 분리하여 관리하기 위한 구조화 도구
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(product_blueprint, url_prefix="/product")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)