from . import db

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_location = db.Column(db.String(255))
    orders = db.relationship("Order", backref="truck")
