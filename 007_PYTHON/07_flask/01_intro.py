from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>타이틀</title>
            <style>
                p {
                    color: red;
                }
            </style>
        </head>
        <body>
            <h1>웰컴 투 마이 홈</h1>
            <p>여기는 텍스트 본문이 들어갑니다.</p>
            <p>여기는 텍스트 본문이 들어갑니다.</p>
        </body>
    """

if __name__ == "__main__":
    # debug=True: 변경 사항이 실행 중에도 반영됨
    app.run(debug=True)