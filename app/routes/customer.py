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