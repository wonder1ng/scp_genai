from flask import Flask, jsonify, render_template, request

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


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/user")
@app.route("/user/<int:user_id>")
def user(user_id= None):
    return render_template("user.html", user_id=user_id, users=users)

@app.route("/product")
def product():
    id = request.args.get("id", type=int)
    name = request.args.get("name", type=str)
    found = products.values()
    if id: 
        found = [p for p in found if p.get("id") == id]
    if name: 
        found = [p for p in found if p.get("name").lower() == name.lower()]
    
    return render_template("product.html", results=found)

if __name__ == "__main__":
    app.run(debug=True)