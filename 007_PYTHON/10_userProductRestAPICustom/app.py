from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "홍길동", "email": "hong@example.com"},
    2: {"id": 2, "name": "김철수", "email": "kim@example.com"},
    3: {"id": 3, "name": "이영희", "email": "lee@example.com"},
    4: {"id": 4, "name": "박민수", "email": "park@example.com"},
    5: {"id": 5, "name": "최지우", "email": "choi@example.com"},
}

products = {
    101: {"id": 101, "name": "Laptop", "price": 1200},
    102: {"id": 102, "name": "Keyboard", "price": 80},
    103: {"id": 103, "name": "Mouse", "price": 40},
    104: {"id": 104, "name": "Monitor", "price": 300},
    105: {"id": 105, "name": "Headset", "price": 150},
}

# 정적 라우팅
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/user")
@app.route("/api/user/<int:id>", methods=['GET'])
def userGet(id=None):
    if id:
        if request.method == "GET":
            res = users.get(id)
            print(res)
            if res: return jsonify(res)
            else: return jsonify(list(users.values()))
        
    return send_from_directory("static", "user.html")

@app.route("/api/user/<int:id>", methods=['POST'])
def userPost(id=None):
    data = request.get_json()
    data["id"] = id
    print(data)
    users[data["id"]] = data
    return jsonify(users.get(id))

@app.route("/api/user/<int:id>", methods=['PATCH'])
def userPatch(id=None):
    data = request.get_json()
    data["id"] = id
    print(data)
    del users[data["oldId"]]
    del data["oldId"]
    users[data["id"]] = data
    return jsonify(users.get(id))

@app.route("/api/user/<int:id>", methods=['DELETE'])
def userDelete(id=None):
    del users[id]
    return jsonify(list(users.values()))

@app.route("/product")
@app.route("/api/product/<int:id>", methods=['GET'])
def productGet(id=None):
    print(id)
    if id:
        if request.method == "GET":
            res = products.get(id)
            print(res)
            if res: return jsonify(res)
            else: return jsonify(list(products.values()))
        
    return send_from_directory("static", "product.html")

@app.route("/api/product/<int:id>", methods=['POST'])
def productPost(id=None):
    data = request.get_json()
    data["id"] = id
    print(data)
    products[data["id"]] = data
    return jsonify(products.get(id))

@app.route("/api/product/<int:id>", methods=['PATCH'])
def productPatch(id=None):
    data = request.get_json()
    data["id"] = id
    print(data)
    del products[data["oldId"]]
    del data["oldId"]
    products[data["id"]] = data
    return jsonify(products.get(id))

@app.route("/api/product/<int:id>", methods=['DELETE'])
def productDelete(id=None):
    del products[id]
    return jsonify(list(products.values()))


if __name__ == "__main__":
    app.run(debug=True)