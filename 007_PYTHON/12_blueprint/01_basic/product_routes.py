from flask import Blueprint, render_template

product_blueprint = Blueprint("product", __name__)

@product_blueprint.route("/")
def product_page():
    return render_template("product.html")

@product_blueprint.route("/detail")
def product_detail_page():
    return render_template("productDetail.html")