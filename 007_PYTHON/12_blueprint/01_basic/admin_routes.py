from flask import Blueprint, render_template

admin_blueprint = Blueprint("admin", __name__)
# Blueprint: 해당 url 주소를 root로 @app.route처럼 사용하게 함
@admin_blueprint.route("/")
def admin_page():
    return render_template("admin.html")