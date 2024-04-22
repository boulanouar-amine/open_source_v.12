
from flask import Flask
from datetime import datetime, timedelta

from .models import db
from .models.customer import Customer
from .models.panier import Panier
from .models.product import Product
from .models.order import Order
from .models.warehouse import ProductStock,Warehouse

from .routes.customer import customer_bp
from .routes.product import product_bp
from .routes.order import order_bp
from .routes.panier import panier_bp 

from .routes.routes import main


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)
    
    app.register_blueprint(customer_bp)
    app.register_blueprint(panier_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)

     
    app.register_blueprint(main)
    
    with app.app_context():
        from .routes import routes
        db.create_all()
        seed_database() 
        return app
    
def seed_database():
    
    current_time = datetime.now()

    # Check if the database is empty, and if so, seed it
    if not Customer.query.first():  # Example check
        customer1 = Customer(id=1,nom='Doe', prenom='John', adresse='1234 Elm St', telephone='123-456-7890')
        customer2 = Customer(id=2,nom='Smith', prenom='Jane', adresse='5678 Oak St', telephone='987-654-3210')
        
        product1 = Product(id=1 ,nom='Laptop', price=1200.00,weight=12)
        product2 = Product(id=2,nom='Phone', price=800.00,weight=123)

        order1 = Order(product_id=1, customer_id=1, quantity=1, start_delivery_date = current_time,end_delivery_date=current_time + timedelta(days=2))
        order2 = Order(product_id=2, customer_id=1, quantity=2, start_delivery_date = current_time,end_delivery_date=current_time + timedelta(days=3))

        db.session.add_all([customer1, customer2, product1, product2, order1, order2])
        db.session.commit()    