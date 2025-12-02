from flask import Blueprint, jsonify, request
from flask_login import login_user, current_user, login_required, logout_user
from app.models import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "customer")   # optional

    if User.query.filter_by(email=email).first():
        return {"error": "Email already registered"}, 400

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {"message": "Signup successful"}, 201



@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid email or password"}, 401

    login_user(user)
    return {"message": "Login successful", "user": user.id}



@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return {"message": "Logged out successfully"}



@auth_bp.route("/me")
def me():
    if current_user.is_authenticated:
        return {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role
        }
    return {"user": None}
