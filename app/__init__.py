
from flask import Flask
from .models import db

from .models.customer import Customer
from .models.panier import Panier
from .models.product import Product
from .models.order import Order
from .models.warehouse import Product_stock,Warehouse

from .routes import main


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)
    
    app.register_blueprint(main)
    
    with app.app_context():
        from . import routes
        db.create_all()
        return app