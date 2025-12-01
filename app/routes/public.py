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



@public_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)

    data = {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category": product.category.name if product.category else None,
        "images": [img.image_url for img in product.images],
        "supplier": product.supplier.name,
    }

    return jsonify(data)



@public_bp.route("/products/<int:product_id>/reviews", methods=["GET"])
def get_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()

    data = []
    for r in reviews:
        data.append({
            "id": r.id,
            "rating": r.rating,
            "comment": r.comment,
            "user": r.user.name,
            "created_at": r.created_at.strftime("%Y-%m-%d"),
        })

    return jsonify(data)



@public_bp.route("/products/<int:product_id>/qna", methods=["GET"])
def get_qna(product_id):
    qna = ProductQnA.query.filter_by(product_id=product_id).all()

    data = []
    for q in qna:
        data.append({
            "id": q.id,
            "question": q.question,
            "answer": q.answer,
            "user": q.user.name,
            "created_at": q.created_at.strftime("%Y-%m-%d"),
        })

    return jsonify(data)