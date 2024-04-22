from app import db

class Product_stock(db.Model):
    __tablename__ = 'product_stock'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Assuming the Product model is defined and has an 'id' column
    product = db.relationship('Product', backref=db.backref('stock', lazy='select'))

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)
    product_stock_list = db.relationship("Product_stock", backref="warehouse")
