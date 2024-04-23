from flask import Flask
from datetime import datetime, timedelta

from .models import db
from .models.customer import Customer
from .models.product import Product
from .models.order import Order
from .models.address import Address
from .models.warehouse import ProductStock, Warehouse
from .routes.customer import customer_bp
from .routes.product import product_bp
from .routes.order import order_bp
from .routes.main import main_bp

def init_warehouse():
    # Check if any warehouse exists
    if Warehouse.query.first() is None:
        # If no warehouse exists, create one
        latitude = 32.89735584205886
        longitude = -6.914085770573746
        new_address = Address(latitude=latitude, longitude=longitude, is_source=True)
        db.session.add(new_address)
        db.session.commit()

        warehouse = Warehouse(nom='Warehouse ENSA', address_id=new_address.id)
        db.session.add(warehouse)
        db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

    app.register_blueprint(customer_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        seed_database()
        init_warehouse()  # Initialize the warehouse if it doesn't exist
        return app

def seed_database():
    current_time = datetime.now()

    # Example of seeding the database with initial data
    if not Customer.query.first():  # Check if the first customer exists
        product1 = Product(nom='Laptop', price=1200.00, weight=1.2)
        product2 = Product(nom='Phone', price=800.00, weight=0.123)

        order1 = Order(product_id=1, customer_id=1, quantity=1, start_delivery_date=current_time, end_delivery_date=current_time + timedelta(days=2))
        order2 = Order(product_id=2, customer_id=1, quantity=2, start_delivery_date=current_time, end_delivery_date=current_time + timedelta(days=3))

        db.session.add_all([product1, product2, order1, order2])
        db.session.commit()

