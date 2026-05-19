from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "asdqwe"

items = [
    {"id": "item1", "name": "apple", "price": 1000},
    {"id": "item2", "name": "banana", "price": 2000},
    {"id": "item3", "name": "cherry", "price": 3000},
]
users = [
    {"name": "Alice", "id": "alice", "pw": "alice"},
    {"name": "Bob", "id": "bob", "pw": "bob1234"},
    {"name": "Charlie", "id": "charlie", "pw": "hello"},
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/product")
def product():
    return render_template("product.html", items=items)

@app.route("/add_to_cart/<item_id>")
def add_to_cart(item_id):
    if session.get("user"):
        print("장바구니에 담을 상품: ", item_id)
        if "cart" not in session:
            session["cart"] = {}
        
        if item_id in session["cart"]:
            session["cart"][item_id] += 1
        else:
            session["cart"][item_id] = 1
        
        print(session["cart"])
        session.modified = True
        item = [item for item in items if item["id"] == item_id][0]
        flash(f"{item["id"]}: {item["name"]}이(가) 장바구니에 담겼습니다.")
        print(f"{item["id"]}: {item["name"]}이(가) 장바구니에 담겼습니다.")

        return redirect(url_for("product"))

    else:
        flash(f"장바구니에 물건을 담기 위해 로그인을 먼저 진행해주세요.")
        return redirect(url_for("login"))

@app.route("/delete_from_cart/<item_id>")
def delete_from_cart(item_id):
    if session["cart"].get(item_id):
        session["cart"][item_id] -= 1
        item = [item for item in items if item["id"] == item_id][0]
        if session["cart"][item_id] == 0:
            del session["cart"][item_id]
            flash(f"장바구니의 물건이 모두 제거되었습니다.")
            print(f"장바구니의 물건이 모두 제거되었습니다.")
            return redirect(url_for("cart"))
        flash(f"{item["id"]}: {item["name"]}이(가) 장바구니에서 1개 제거되었습니다.")
        print(f"{item["id"]}: {item["name"]}이(가) 장바구니에서 1개 제거되었습니다.")
    else:
        session["cart"] = {}
        flash(f"장바구니의 물건이 모두 제거되었습니다.")
        print(f"장바구니의 물건이 모두 제거되었습니다.")
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    if session.get("user"):
        cart_items = {}
        total_price = 0
        for item_id, quantity in session.get("cart", {}).items():
            item = next((item for item in items if item["id"] == item_id), None)
            cart_items[item_id] = {
                "name": item["name"] ,
                "quantity": quantity,
                "price": item["price"]
            }
            total_price += item["price"] * quantity
        return render_template("cart.html", cart_items=cart_items, total_price=total_price)
    else:
        flash(f"장바구니에 물건을 담기 위해 로그인을 먼저 진행해주세요.")
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        user = session.get("user")
        if user:
            session["user"] = user
            return render_template("login.html", user = user)
        else:
            return render_template("login.html")
    elif request.method == "POST":
        id = request.form.get("id")
        pw = request.form.get("pw")

        user = next((u for u in users if u["id"] == id and u["pw"] == pw), None)
        print(user)
        if user:
            session["user"] = user
            return render_template("login.html", user = user)
        else:
            error = "Invalid ID or password"
        return render_template("login.html", error = error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session["cart"] = {}
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)