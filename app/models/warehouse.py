from . import db

class Product_stock(db.Model):
    __tablename__ = 'product_stock'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Corrected ForeignKey reference
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)  # Link to Warehouse
    quantity = db.Column(db.Integer, nullable=False)
    
    product = db.relationship('Product', backref=db.backref('stock', lazy='select'))

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)
    product_stock_list = db.relationship("Product_stock", backref="warehouse")

    