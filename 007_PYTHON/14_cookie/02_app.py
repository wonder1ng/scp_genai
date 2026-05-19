from flask import Flask, make_response, request

app = Flask(__name__)

@app.route("/")
def main():
    cookie = request.cookies.get("my-data")
    if cookie:
        return f"안녕 {cookie} 야"
    else:
        resp = make_response("첫 방문이시군요. 또 오세요.")
        resp.set_cookie("my-data", "spc2026")
        return resp

if __name__ == "__main__":
    app.run(debug=True) 