from . import db

class Product_stock(db.Model):
    __tablename__ = 'product_stock'
    
    id = db.Column(db.Integer, primary_key=True)
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Corrected ForeignKey reference
    product = db.relationship(
        'Product', backref=db.backref('stock', lazy='select'))
    
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)  # Link to Warehouse
    Warehouse = db.relationship('Warehouse', backref=db.backref('product_stock', lazy='select'))  # Link to Warehouse
    
    quantity = db.Column(db.Integer, nullable=False)
    
    
class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    
    id = db.Column(db.Integer, primary_key=True)
    product_stock_list = db.relationship("Product_stock", backref="warehouse")

    