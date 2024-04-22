from . import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String)
    prenom = db.Column(db.String)
    address = db.relationship(
        'Address', back_populates='customer', uselist=False)

    telephone = db.Column(db.String)

    orders = db.relationship('Order', back_populates='customer', overlaps="orders")

