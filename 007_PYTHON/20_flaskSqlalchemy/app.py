from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        # print할 때 아래 형식으로 출력됨
        return f"<User {self.id}, {self.name}, {self.age}>"
    
base_path = "\\".join(__file__.split("\\")[:-1])
app = Flask(__name__)
app.config["SECRET_KEY"] = "my-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{base_path}\\example.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def index():
    users = User.query.all()
    for user in users:
        print(user)
    return render_template("index.html", users=users)

if __name__ == "__main__":
    with app.app_context():
        print("DB 초기화 중")
        db.create_all()

        if not User.query.first():
            print("사용자 초기화")
            user1 = User(name="user1", age=30)
            user1 = User(name="user2", age=33)
            user1 = User(name="user3", age=34)