from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_cors import CORS 

from .extensions import db, migrate, login_manager
from .routes.public import public_bp
from .routes.customer import customer_bp
from .routes.supplier import supplier_bp
from .routes.admin import admin_bp
from .routes.auth import auth_bp
import os


def create_app(config_class=None):
    app = Flask(__name__)

    # ------------------------------------
    # CONFIG
    # ------------------------------------
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config['SECRET_KEY'] = "ecommercesite"
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecommerce.db"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    
    # ------------------------------------
    # EXTENSIONS
    # ------------------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # all React front-end to communite
    CORS(app, supports_credentials=True)

    # ------------------------------------
    # BLUEPRINTS
    # ------------------------------------
    app.register_blueprint(public_bp, url_prefix="/api")
    app.register_blueprint(customer_bp, url_prefix="/api/customer")
    app.register_blueprint(supplier_bp, url_prefix="/api/supplier")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")


    return app