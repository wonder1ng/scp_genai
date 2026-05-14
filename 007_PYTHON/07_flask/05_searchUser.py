from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"name": "Alice", "age": 25, "phone": "123-456-7890"},
    {"name": "Bob", "age": 30, "phone": "123-555-7890"},
    {"name": "Charlie", "age": 27, "phone": "123-777-7890"},
    {"name": "David", "age": 25, "phone": "123-888-7890"},
]

@app.route("/search")
def search_user():
    name = request.args.get("name")
    age = request.args.get("age")
    phone = request.args.get("phone")

    result = [user for user in users if user.get("name").lower() == name.lower()] if name else users
    result = [user for user in result if user.get("age") == int(age)] if age else result
    # result = [user for user in result if user.get("phone") == phone] if phone else result
    result = [user for user in result if user.get("phone").startswith(phone)] if phone else result

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)