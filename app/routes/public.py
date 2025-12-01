from flask import Blueprint, jsonify, request
from app.models import Product, ProductImage, Review, ProductQnA

public_bp = Blueprint("public", __name__)

@public_bp.route("/status")
def status():
    return jsonify({"message": "Public API working"})



@public_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()

    data = []
    for p in products:
        data.append({
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "stock": p.stock,
            "thumbnail": p.thumbnail,
            "category": p.category.name if p.category else None,
        })

    return jsonify(data)