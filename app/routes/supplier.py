from flask import Blueprint, jsonify

supplier_bp = Blueprint("supplier", __name__)

@supplier_bp.route("/status")
def status():
    return jsonify({"message": "Supplier API working"})