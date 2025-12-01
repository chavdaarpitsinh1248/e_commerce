from flask import Blueprint, jsonify

public_bp = Blueprint("public", __name__)

@public_bp.route("/status")
def status():
    return jsonify({"message": "Public API working"})