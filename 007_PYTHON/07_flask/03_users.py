from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"name": "Alice", "age": 25, "phone": "123-456-7890"},
    {"name": "Bob", "age": 30, "phone": "123-555-7890"},
    {"name": "Charlie", "age": 27, "phone": "123-777-7890"},
    {"name": "David", "age": 25, "phone": "123-888-7890"},
]

@app.route("/")
def main():
    # return f"<h1>메인 페이지</h1>"
    return jsonify(users)

@app.route("/user/<name>")
def get_user_by_name(name):
    print("사용자 입력값:", name)
    user = None
    for u in users:
        if u["name"].lower() == name.lower():
            user = u
    if user: return jsonify(user)
    else: return jsonify({"message": "사용자를 찾지 못했습니다."})
    
if __name__ == "__main__":
    app.run(debug=True)