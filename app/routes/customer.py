from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.models import Cart, CartItem, Product, Order, OrderItem
from app.extensions import db


customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/status")
def status():
    return jsonify({"message": "Customer API working"})

def get_or_create_cart(user):
    if user.cart:
        return user.cart
    
    cart = Cart(user_id=user.id)
    db.session.add(cart)
    db.session.commit()
    return cart



@customer_bp.route("/cart/add", methods=["POST"])
@login_required
def add_to_cart():
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    product = Product.query.get_or_404(product_id)

    cart = get_or_create_cart(current_user)

    # Check if item exists
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product.id, quantity=quantity)
        db.session.add(item)

    db.session.commit()

    return jsonify({"message": "Item added to cart"}), 200



@customer_bp.route("/cart", methods=["GET"])
@login_required
def get_cart():
    cart = get_or_create_cart(current_user)

    items = []
    for i in cart.items:
        items.append({
            "id": i.id,
            "product_id": i.product_id,
            "title": i.product.title,
            "price": i.product.price,
            "quantity": i.quantity,
            "thumbnail": i.product.thumbnail
        })

    return jsonify({
        "cart_id": cart.id,
        "items": items
    })
    


@customer_bp.route("/cart/update", methods=["PUT"])
@login_required
def update_cart_item():
    data = request.json
    item_id = data.get("item_id")
    quantity = data.get("quantity")

    item = CartItem.query.get_or_404(item_id)

    # Ensure the user owns this item
    if item.cart.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    item.quantity = quantity
    db.session.commit()

    return jsonify({"message": "Quantity updated"})



@customer_bp.route("/cart/remove/<int:item_id>", methods=["DELETE"])
@login_required
def remove_item(item_id):
    item = CartItem.query.get_or_404(item_id)

    if item.cart.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item removed"})



@customer_bp.route("/cart/clear", methods=["DELETE"])
@login_required
def clear_cart():
    cart = get_or_create_cart(current_user)

    for item in cart.items:
        db.session.delete(item)
    
    db.session.commit()

    return jsonify({"message": "Cart cleared"})



@customer_bp.route("/checkout", methods=["POST"])
@login_required
def checkout():
    cart = get_or_create_cart(current_user)

    if not cart.items:
        return jsonify({"error": "Cart is empty"}), 400
    
    total = 0
    for item in cart.items:
        total += item.product.price * item.quantity

    # Create order
    order = Order(user_id=current_user.id, total_amount=total)
    db.session.add(order)
    db.session.commit()

    # Add items to order
    for item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)


    # Clear cart 
    for item in cart.items:
        db.session.delete(item)
    
    db.session.commit()

    return jsonify({
        "message": "Order created",
        "order_id": order.id,
        "total": total
    })