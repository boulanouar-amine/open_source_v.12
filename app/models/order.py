from . import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    
    panier_id = db.Column(db.Integer, db.ForeignKey('paniers.id'))
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product', backref='orders')
    
    quantity = db.Column(db.Integer, nullable=False)
    
    start_delivery_date = db.Column(db.Date, nullable=False)
    end_delivery_date = db.Column(db.Date, nullable=False)
    
    delivery_address = db.Column(db.String, nullable=False)
    # weight is calculated as the sum of the weight of the products in the order
    order_weight = db.Column(db.Float, nullable=False)