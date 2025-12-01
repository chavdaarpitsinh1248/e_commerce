from flask import Blueprint, jsonify

customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/status")
def status():
    return jsonify({"message": "Customer API working"})