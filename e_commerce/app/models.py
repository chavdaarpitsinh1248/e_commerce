from app import db, login_manager
import os
from flask import url_for
from flask_login import UserMixin
from datetime import datetime

# ---------------------------------
#               LOGIN LOADER
# ---------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# association table for many-to-many between Manga and Genre
#manga_genre = db.Table(
#    'manga_genre',
#    db.Column('manga_id', db.Integer, db.ForeignKey('manga.id'), primary_key=True),
#    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
#)



# -----------------------------------------
#                      USER
#   (Customer / Supplier / Staff / Admin)
# -----------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="customer")
    # roles = customer, supplier, staff, admin

    profile_pic = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def profile_pic_url(self):
        if self.profile_pic:
            name = os.path.basename(self.profile_pic)
            return url_for('static', filename=f'uploads/profile_pics/{name}')
        return url_for('static', filename='images/default_user.png')

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

# ------------------------------------------
#               SUPPLIER PROFILE
# ------------------------------------------
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)

    store_name = db.Column(db.String(150), nullable=False)
    store_description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('supplier_profile', uselist=False))

    def __repr__(self):
        return f"<Supplier {self.store_name}>"

# ----------------------------------------
#               STAFF / ADMIN
# ----------------------------------------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    role = db.Column(db.String(40), default='staff')
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

#       is_admin = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='staff_profile', lazy=True)

    def __repr__(self):
        return f"<Staff {self.user.username} ({self.role})>"

# ----------------------------------------
#              CATEGORY
# ----------------------------------------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"

# ----------------------------------------
#               BRAND
# ----------------------------------------
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Brand {self.name}>"


# ---------------------------------------
#               PRODUCT
# ---------------------------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)

    stock = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    
    supplier = db.relationship('Supplier', backref=db.backref('products', lazy=True))
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    brand = db.relationship('Brand', backref=db.backref('products', lazy=True))

    images = db.relationship("ProductImage", backref="product", lazy=True,
                                        cascade="all, delete-orphan")

    reviews = db.relationship("Review", backref="product", lazy=True,
                                        cascade="all, delete-orphan")

    questions = db.relationship("Question", backref="product", lazy=True,
                                        cascade="all, delete-orphan")

       
    @property
    def discounted_price(self):
        return self.price - (self.price * self.discount / 100)

    def __repr__(self):
        return f"<Product {self.title}>"

# ---------------------------------
#               PRODUCT IMAGES
# ---------------------------------
class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    image_path = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f"<ProductImage product: {self.product_id})>"


# ---------------------------------
#               CART
# ---------------------------------
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True, cascade="all, delete-orphan"))
    product = db.relationship('Product')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='_user_product_cart_uc'),
        )

    def __repr__(self):
        return f"<CartItem U:{self.user_id} P:{self.product_id}>"

# ---------------------------------
#               ORDERS
# ---------------------------------
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    status = db.Column(db.String(40), default="pending")
    # pending / paid / shipped / delivered / cancelled
    

    def __repr__(self):
        return f"<Comment {self.id} by User:{self.user_id}>"

# ---------------------------------
#               LIKE
# ---------------------------------
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    manga_id = db.Column(db.Integer, db.ForeignKey('manga.id'), nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('likes', lazy=True, cascade="all, delete-orphan"))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'manga_id', name='_user_manga_like_uc'),
        db.UniqueConstraint('user_id', 'chapter_id', name='_user_chapter_like_uc'),
    )

    def __repr__(self):
        if self.chapter_id:
            return f"<Like User:{self.user_id} Chapter:{self.chapter_id}>"
        return f"<Like User:{self.user_id} Manga:{self.manga_id}>"

# ---------------------------------
#               NOTIFICATION
# ---------------------------------
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    is_read = db.Column(db.Boolean, default=False, index=True)
    message = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<Notification to:{self.user_id} message:{self.message[:25]}>"

# ---------------------------------
#               GENRE
# ---------------------------------
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Genre {self.name}>"

