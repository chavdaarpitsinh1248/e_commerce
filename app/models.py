from datetime import datetime
from app.extensions import db, login_manager
from flask_login import UserMixin


# ----------------------------------------------------------------
# LOGIN LOADER
# ----------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# ----------------------------------------------------------------
# USER MODEL
# ROLES: customer, suppllier, staff, admin
# ----------------------------------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="customer")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    products = db.relationship("Product", backref="supplier", lazy=True)
    cart = db.relationship("Cart", backref="user", uselist=False)
    orders = db.relationship("Order", backref="user", lazy=True)

    def is_admin(self):
        return self.role == "admin"
    
    def is_supplier(self):
        return self.role == "supplier"



# ----------------------------------------------------------------
# CATEGORY MODEL
# ----------------------------------------------------------------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    products = db.relationship("Product", backref="category", lazy=True)



# ----------------------------------------------------------------
# PRODUCT MODEL
# ----------------------------------------------------------------

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    supplier_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    thumbnail = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship("ProductImage", backref="product", lazy=True)
    reviews = db.relationship("Review", backref="product", lazy=True)
    qna = db.relationship("ProductQnA", backref="product", lazy=True)



# ----------------------------------------------------------------
# PRODUCT IMAGES
# ----------------------------------------------------------------
class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)    



# ----------------------------------------------------------------
# CART MODEL
# one cart per user
# ----------------------------------------------------------------    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), unique=True)

    items = db.relationship("CartItem", backref="cart", lazy=True, cascade="all, delete")



# ----------------------------------------------------------------
# CART ITEMS
# ----------------------------------------------------------------
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    quantity = db.COlumn(db.Integer, default=1)

    product = db.relationship("Product")



# ----------------------------------------------------------------
# ORDER MODEL
# ----------------------------------------------------------------
