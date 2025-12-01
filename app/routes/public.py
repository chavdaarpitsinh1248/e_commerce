from flask import Blueprint, jsonify, request
from app.models import Product, ProductImage, Review, ProductQnA

public_bp = Blueprint("public", __name__)

@public_bp.route("/status")
def status():
    return jsonify({"message": "Public API working"})