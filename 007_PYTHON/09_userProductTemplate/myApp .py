# from flask import Flask, jsonify, render_template, request

# app = Flask(__name__)


# users = {
#     1: {"id": 1, "name": "홍길동", "email": "hong@example.com"},
#     2: {"id": 2, "name": "김철수", "email": "kim@example.com"},
#     3: {"id": 3, "name": "이영희", "email": "lee@example.com"},
#     4: {"id": 4, "name": "박민수", "email": "park@example.com"},
#     5: {"id": 5, "name": "최지우", "email": "choi@example.com"},
# }

# products = {
#     101: {"id": 101, "name": "Laptop", "price": 1200},
#     102: {"id": 102, "name": "Keyboard", "price": 80},
#     103: {"id": 103, "name": "Mouse", "price": 40},
#     104: {"id": 104, "name": "Monitor", "price": 300},
#     105: {"id": 105, "name": "Headset", "price": 150},
# }


# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/user/<q>")
# def user(q):
#     result = users.get(int(q)) if q.isdigit() else [v for v in users.values() if v.get("name") == q]
#     if result and type(result) == list: result = result[0]
#     if result: return render_template("user.html", user=result)
#     # if result: render_template("user.html", id=result["id"], name=result["name"], email=result["email"])
#     else: return render_template("user.html", user={"id": None, "name": None, "email": None})

# @app.route("/product")
# def product():
#     id = request.args.get("id")
#     name = request.args.get("name")
#     print("name".isdigit())
#     if id: 
#         result = products.get(int(id)) if id.isdigit() else {"id": None, "name": None, "price": None}
#     if name: 
#         result = [v for v in products.values() if v.get("name") == name]
#         if not result:
#             result = {"id": None, "name": None, "price": None}
#     if result: return render_template("product.html", product=result)
#     else: return render_template("product.html", product={"id": None, "name": None, "price": None})



# if __name__ == "__main__":
#     app.run(debug=True)