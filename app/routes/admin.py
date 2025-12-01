from flask import Blueprint, jsonify

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/status")
def status():
    return jsonify({"message": "Admin API working"})