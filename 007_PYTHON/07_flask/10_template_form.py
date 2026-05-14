import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# 저장소 설정
app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def index():
    return render_template("form.html")


def allowed_file(filename):
    ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/login", methods=["POST"])
def login():
    id = request.form.get("id")
    pw = request.form.get("pw")
    print(f"입력한 ID는 {id}, PW는 {pw}")
    return render_template("login.html", name=id)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["photo"]
    filename = file.filename

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        return "파일 잘 받았음"
    else:
        return f"지원되지 않는 파일입니다. 파일명: {file.filename}"

if __name__ == "__main__":
    app.run(debug=True)