from . import db

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True)
    # Define the relationship here, but without using the `back_populates` just yet
    product_stocks = db.relationship('ProductStock', overlaps="product_stocks")

class ProductStock(db.Model):
    __tablename__ = 'product_stocks'
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    warehouse = db.relationship('Warehouse', back_populates='product_stocks')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship(
        'Product', backref=db.backref('stock', lazy='select'))
    quantity = db.Column(db.Integer, nullable=False)

# Now set up back_populates after both classes have been defined
Warehouse.product_stocks = db.relationship('ProductStock', back_populates='warehouse', overlaps="product_stocks")
