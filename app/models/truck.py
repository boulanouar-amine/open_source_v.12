from . import db


class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    
    current_address = db.relationship(
        'Address', back_populates='truck', uselist=False)
    
    destination = db.relationship(
        'Address', back_populates='truck', uselist=False)
    
    orders = db.relationship("Order", backref="truck")
    
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    warehouse = db.relationship('Warehouse', backref='trucks')
