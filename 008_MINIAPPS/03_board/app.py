from flask import Flask, jsonify, request, send_from_directory
from database import MyDatabase

app = Flask(__name__)
db = MyDatabase()
table_name = "board"
# @app.route("/")
# def index():
#     return send_from_directory("static", "index.html")
# # staticfile 연결법
# @app.route("/js/<path:filename>")
# def serve_js(filename):
#     return send_from_directory("static/js", filename)
@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

@app.route("/create", methods=["POST"])
def create():
    res = request.get_json()
    db.execute(f"insert into {table_name} (title, content) values (?,?);", (res["title"], res["content"]))
    db.commit()
    return jsonify({"result": "success"})

@app.route("/list")
def list():
    res = db.excute_fetch(f"select * from {table_name}")
    return jsonify({"result": "success", "body": res})

@app.route("/delete", methods=["DELETE"])
def delete():
    res = request.get_json()
    db.execute(f"delete from {table_name} where id=?", [res["id"]])
    db.commit()
    return jsonify({"result": "success"})

@app.route("/modify", methods=["PUT"])
def modify():
    res = request.get_json()
    print(res)
    db.execute(f"update {table_name} set title=?, content=? where id=?", (res["title"], res["content"], res["id"]))
    db.commit()
    print("done!!")
    return jsonify({"result": "success"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)