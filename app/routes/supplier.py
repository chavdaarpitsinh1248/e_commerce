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
    if not ok:
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



@supplier_bp.route("/product/<int:product_id>/add-image", methods=["POST"])
@login_required
def add_image(product_id):
    ok, res, code = supplier_required()
    if not ok:
        return res, code

    product = Product.query.get_or_404(product_id)

    # supplier must own product
    if product.supplier_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.json
    image_url = data.get("image_url")

    img = ProductImage(product_id=product.id, image_url=image_url)
    db.session.add(img)
    db.session.commit()

    return jsonify({"message": "Image added"})



@supplier_bp.route("/product/<int:product_id>/update", methods=["PUT"])
@login_required
def update_product(product_id):
    ok, res, code = supplier_required()
    if not ok:
        return res, code

    product = Product.query.get_or_404(product_id)

    if product.supplier_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    data  = request.json

    product.title = data.get("title", product.title)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.category_id = data.get("category_id", product.category_id)
    product.thumbnail = data.get("thumbnail", product.thumbnail)

    db.session.commit()

    return jsonify({"message": "Product updated"})



@supplier_bp.route("/product/<int:product_id>/stock", methods=["PUT"])
@login_required
def update_stock(product_id):
    ok, res, code = supplier_required()
    if not ok:
        return res, code

    product = Product.query.get_or_404(product_id)

    if product.supplier_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.json
    new_stock = data.get("stock")

    product.stock = new_stock
    db.session.commit()

    return jsonify({"message": "Stock updated"})



@supplier_bp.route("/my-products", methods=["GET"])
@login_required
def my_products():
    ok, res, code = supplier_required()
    if not ok:
        return res, code

    products = Product.query.filter_by(supplier_id=current_user.id).all()

    data = []
    for p in products:
        data.append({
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "stock": p.stock,
            "thumbnail": p.thumbnail
        })

        return jsonify(data)