from . import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    
    panier_id = db.Column(db.Integer, db.ForeignKey('paniers.id'))
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product', backref='orders')
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customer', back_populates='orders')
    
    quantity = db.Column(db.Integer, nullable=False)
    
    start_delivery_date = db.Column(db.DateTime, nullable=False)
    end_delivery_date = db.Column(db.DateTime, nullable=False)
    
    # weight is calculated as the sum of the weight of the products in the order
    order_weight = db.Column(db.Float, nullable=True)