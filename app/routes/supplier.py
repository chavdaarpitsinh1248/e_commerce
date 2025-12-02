from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.models import Product, ProductImage, Category
from app.extensions import db


supplier_bp = Blueprint("supplier", __name__)


def supplier_required():
    if not current_user.is_authenticated:
        return False, jsonify({"error": "Lofin required"}), 401
    if current_user.role != "supplier":
        return False, jsonify({"error": "Supplier access only"}), 403
    
    return True, None, None



@supplier_bp.route("/status")
def status():
    return jsonify({"message": "Supplier API working"})



@supplier_bp.route("/add-product", methods=["POST"])
@login_required
def add_product():
    ok, res, code = supplier_required()
    if not pk:
        return res, code
    
    data = request.json

    product = Product(
        supplier_id=current_user.id,
        title=data.get("title"),
        description=data.get("description"),
        price=data.get("price"),
        stock=data.get("stock"),
        category_id=data.get("category_id"),
        thumbnail=data.get("thumbnail") # can be null
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created",
        "product_id": product.id
    })