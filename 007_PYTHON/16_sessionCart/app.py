from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "asdqwe"

items = [
    {"id": "item1", "name": "햄버거", "price": 3000},
    {"id": "item2", "name": "핫도그", "price": 2000},
    {"id": "item3", "name": "콜리", "price": 1500},
]


@app.route("/")
def index():
    return render_template("product.html", items=items)

@app.route("/add_to_cart/<item_id>")
def add_to_cart(item_id):
    print("장바구니에 담을 상품: ", item_id)
    if "cart" not in session:
        session["cart"] = {}
    
    if item_id in session["cart"]:
        session["cart"][item_id] += 1
    else:
        session["cart"][item_id] = 1
    
    print(session["cart"])
    session.modified = True   # 세션 데이터가 수정되었음을 flask에게 인지시킴
    
    # flash: 1회성 변수로 session에 임시 저장되어 호출되며 제거됨
    flash(f"{[item for item in items if item["id"] == item_id][0]['name']}이(가) 장바구니에 추가되었습니다.")
    print(f"{[item for item in items if item["id"] == item_id][0]['name']}이(가) 장바구니에 추가되었습니다.")

    return redirect(url_for("index"))
    

@app.route("/cart")
def view_cart():
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
    

if __name__ == "__main__":
    app.run(debug=True)